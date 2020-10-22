import base64
import os
import re

import requests
from celery import shared_task
from django.contrib.sites.models import Site
from django.db.models import Q
from django.shortcuts import get_object_or_404
from django.template.loader import get_template
from django.urls import reverse
from django.utils import timezone

from .models import Node


def tiny_to_page_id(tiny):
    # https://community.atlassian.com/t5/Confluence-questions/What-is-the-algorithm-used-to-create-the-quot-Tiny-links-quot/qaq-p/186555
    return int.from_bytes(
        base64.b64decode(
            tiny.ljust(8, "A").replace("_", "+").replace("-", "/").encode()
        ),
        byteorder="little",
    )


def get_node_attrs(instance):
    attributes = {}
    schema_properties = instance.nodetype.attribute_schema.schema["properties"]
    for key, value in instance.attributeSet.items():
        if key in schema_properties:
            if "title" in schema_properties[key]:
                attributes[schema_properties[key]["title"]] = value
            else:
                attributes[key] = value
    attributes["Domain/Subsystem or Subdomain"] = ""
    attributes["Service/Component Responsible"] = instance.attributeSet["name"]
    attributes["Contact"] = ""
    attributes["Service/Component Status"] = instance.attributeSet["status"]
    return attributes


def get_outbound_edges(instance, domain):
    outbound_edges = {}

    for edge in instance.outbound_edges.all():
        edgetype = edge.edge_type.edgetype
        if edgetype not in outbound_edges:
            outbound_edges[edgetype] = []
        url = domain + reverse("nodes:node.detail", args=[edge.target.key])
        name = edge.target.attributeSet.get("name")
        item = f'(<a href="http://{url}">{edge.target.key}</a>) {name}'
        outbound_edges[edgetype].append(item)

    return outbound_edges


def get_inbound_edges(instance, domain):
    inbound_edges = {}

    for edge in instance.inbound_edges.all():
        edgetype = edge.edge_type.edgetype
        if edgetype not in inbound_edges:
            inbound_edges[edgetype] = []
        url = domain + reverse("nodes:node.detail", args=[edge.source.key])
        name = edge.source.attributeSet.get("name")
        item = f'(<a href="http://{url}">{edge.source.key}</a>) {name}'
        inbound_edges[edgetype].append(item)

    return inbound_edges


def update_confluence(title, context, doc_url):
    new_spec = get_template("nodes/confluence_page.html").render(context)
    tiny = re.sub(r".*\/", "", doc_url)
    page_id = tiny_to_page_id(tiny)
    apiurl = os.environ["CONFLUENCE_URL"]
    r = requests.get(
        f"{apiurl}/content/{page_id}?expand=version,body.storage",
        headers={"KeyId": os.environ["API_KEY"]},
        auth=(os.environ["CONFLUENCE_USER"], os.environ["CONFLUENCE_PASS"]),
    )

    version = int(re.sub(r".*\/", "", r.json()["version"]["_links"]["self"]))

    data = {
        "id": page_id,
        "type": "page",
        "title": title,
        "body": {"storage": {"value": new_spec, "representation": "storage"}},
        "version": {"number": version + 1},
    }
    r = requests.put(
        f"{apiurl}/content/{page_id}",
        headers={"KeyId": os.environ["API_KEY"]},
        auth=(os.environ["CONFLUENCE_USER"], os.environ["CONFLUENCE_PASS"]),
        json=data,
    )
    print(r.status_code)


def update_confluence_for_component(nodekey):
    instance = get_object_or_404(Node, pk=nodekey)
    doc_system = instance.attributeSet.get("primaryDocumentationSystem")
    doc_url = instance.attributeSet.get("docupediaPage")
    if doc_system != "ARC001" or doc_url == "":
        return

    domain = Site.objects.get_current().domain

    attributes = get_node_attrs(instance)
    outbound_edges = get_outbound_edges(instance, domain)
    inbound_edges = get_inbound_edges(instance, domain)

    if "isDomainOf" in outbound_edges:
        attributes["Domain/Subsystem or Subdomain"] = outbound_edges["isDomainOf"][0]

    if "isResponsibleOf" in outbound_edges:
        attributes["Service/Component Responsible"] = outbound_edges["isResponsibleOf"][
            0
        ]

    if "isContactOf" in outbound_edges:
        attributes["Contact"] = ", ".join(outbound_edges["isContactOf"])

    image_url = "https://www.xxx.com"
    title = f'({instance.key}) {instance.attributeSet["name"]} ({instance.attributeSet["status"]})'
    context = {
        "domain": domain,
        "node": instance,
        "attributes": attributes,
        "inbound_edges": inbound_edges,
        "outbound_edges": outbound_edges,
        "image_url": image_url,
    }

    update_confluence(title, context, doc_url)


@shared_task
def update_component_page_task(nodekey):
    update_confluence_for_component(nodekey)
    print(f"Task: Page for {nodekey} updated!")


@shared_task
def update_components_page_task():
    one_h_ago = timezone.now() - timezone.timedelta(hours=1)
    nodes = Node.objects.filter(Q(nodetype="component") & Q(updated__gte=one_h_ago))
    for node in nodes:
        update_confluence_for_component(node.key)
    print("Task: All components updated!")
