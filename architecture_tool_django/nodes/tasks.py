import logging
import re

from celery import shared_task
from django.conf import settings
from django.db.models import Q
from django.shortcuts import get_object_or_404
from django.template.loader import get_template
from django.urls import reverse
from django.utils import timezone

from architecture_tool_django.utils.confluence_wrapper import (
    MyConfluence,
    tiny_to_page_id,
)

from .models import Node

logger = logging.getLogger(__name__)


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


def get_outbound_edges(instance, base_url):
    outbound_edges = {}

    for edge in instance.outbound_edges.all():
        edgetype = edge.edge_type.edgetype
        if edgetype not in outbound_edges:
            outbound_edges[edgetype] = []
        url = base_url + reverse("nodes:node.detail", args=[edge.target.key])
        name = edge.target.attributeSet.get("name")
        item = f'(<a href="{url}">{edge.target.key}</a>) {name}'
        outbound_edges[edgetype].append(item)

    return outbound_edges


def get_inbound_edges(instance, base_url):
    inbound_edges = {}

    for edge in instance.inbound_edges.all():
        edgetype = edge.edge_type.edgetype
        if edgetype not in inbound_edges:
            inbound_edges[edgetype] = []
        url = base_url + reverse("nodes:node.detail", args=[edge.source.key])
        name = edge.source.attributeSet.get("name")
        item = f'(<a href="{url}">{edge.source.key}</a>) {name}'
        inbound_edges[edgetype].append(item)

    return inbound_edges


def update_confluence(title, context, doc_url):
    new_spec = get_template("misc/confluence_page.html").render(context)
    tiny = re.sub(r".*\/", "", doc_url)
    page_id = tiny_to_page_id(tiny)
    confluence = MyConfluence()
    # page = confluence.get_page_by_id(page_id, expand="version,body.storage")
    # version = int(re.sub(r".*\/", "", r.json()["version"]["_links"]["self"]))
    confluence.update_page(
        page_id,
        title,
        new_spec,
        parent_id=None,
        type="page",
        representation="storage",
        minor_edit=False,
    )


def update_confluence_for_component(nodekey):
    instance = get_object_or_404(Node, pk=nodekey)
    doc_system = instance.attributeSet.get("primaryDocumentationSystem")
    doc_url = instance.attributeSet.get("docupediaPage")
    if doc_system != "ARC001" or doc_url == "":
        return

    base_url = settings.ARCHITECTURE_TOOL_URL

    attributes = get_node_attrs(instance)
    outbound_edges = get_outbound_edges(instance, base_url)
    inbound_edges = get_inbound_edges(instance, base_url)

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
        "base_url": base_url,
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
    logger.info(f"Task: Page for {nodekey} updated!")


@shared_task
def update_components_page_task():
    one_h_ago = timezone.now() - timezone.timedelta(hours=1)
    nodes = Node.objects.filter(Q(nodetype="component") & Q(updated__gte=one_h_ago))
    for node in nodes:
        update_confluence_for_component(node.key)
    logger.info("Task: All components updated!")
