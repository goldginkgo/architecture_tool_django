import json

import gitlab
from celery import shared_task
from django.conf import settings
from django.shortcuts import get_object_or_404
from gitlab.exceptions import GitlabGetError

from architecture_tool_django.graphdefs.api.serializers import GraphSerializer
from architecture_tool_django.graphdefs.models import Graph
from architecture_tool_django.listdefs.api.serializers import ListSerializer
from architecture_tool_django.listdefs.models import List
from architecture_tool_django.modeling.api.serializers import (
    EdgetypeSerializer,
    NodetypeSerializer,
    SchemaSerializer,
)
from architecture_tool_django.modeling.models import Edgetype, Nodetype, Schema
from architecture_tool_django.nodes.api.serializers import NodeSerializer
from architecture_tool_django.nodes.models import Node


def ordered(obj):  # compare json
    if isinstance(obj, dict):
        return sorted((k, ordered(v)) for k, v in obj.items())
    if isinstance(obj, list):
        return sorted(ordered(x) for x in obj)
    else:
        return obj


def get_project(token=None):
    if token is None:
        gl = gitlab.Gitlab(settings.GITLAB_URL, oauth_token=settings.GITLAB_TOKEN)
        project = gl.projects.get(settings.GITLAB_PROJECT_ID)
    else:
        gl = gitlab.Gitlab(settings.GITLAB_URL, oauth_token=token)
        project = gl.projects.get(settings.GITLAB_PROJECT_ID)

    return project


def sync_file(project, filepath, new_content_json):
    new_content = json.dumps(new_content_json, indent=2)
    try:
        f = project.files.get(file_path=filepath, ref="master")
        old_content = json.loads(f.decode())
        json.loads(f.decode())

        if ordered(old_content) == ordered(new_content_json):
            print(f"{filepath} is update to date.")
        else:
            print(f"sync {filepath}")
            f.content = new_content
            f.save(branch="master", commit_message=f"sync {filepath}")
    except GitlabGetError:
        print(f"sync {filepath}")
        project.files.create(
            {
                "file_path": filepath,
                "branch": "master",
                "content": new_content,
                "commit_message": f"sync {filepath}",
            }
        )


def cleanup_files(project, path, allowed_files):
    for item in project.repository_tree(path, all=True):
        filename = item["name"]
        if filename not in allowed_files:
            delete_file(project, path, filename)


def delete_file(project, path, filename):
    print(f"deleting {path}/{filename}")
    project.files.delete(
        file_path=f"{path}/{filename}",
        commit_message=f"delete {path}/{filename}",
        branch="master",
    )


def sync_schemas(token=None):
    project = get_project(token)
    files = []
    for schema in Schema.objects.all():
        files.append(schema.key + ".json")
        serializer = SchemaSerializer(schema)
        sync_file(project, f"modeling/schemas/{schema.key}.json", serializer.data)
    cleanup_files(project, "modeling/schemas", files)


@shared_task
def sync_schema(key, token=None):
    project = get_project(token)
    serializer = SchemaSerializer(get_object_or_404(Schema, pk=key))
    sync_file(project, f"modeling/schemas/{key}.json", serializer.data)


@shared_task
def delete_schema(key, token=None):
    project = get_project(token)
    delete_file(project, "modeling/schemas", f"{key}.json")


@shared_task
def sync_nodetypes(token=None):
    project = get_project(token)
    serializer = NodetypeSerializer(Nodetype.objects.all(), many=True)
    sync_file(project, "modeling/nodetypes.json", serializer.data)


@shared_task
def sync_edgetypes(token=None):
    project = get_project(token)
    serializer = EdgetypeSerializer(Edgetype.objects.all(), many=True)
    sync_file(project, "modeling/edgetypes.json", serializer.data)


def sync_nodes(token=None):
    project = get_project(token)
    folder_files = {}
    for node in Node.objects.all():
        path = f"nodes/{node.nodetype.folder}"
        filename = f"{node.key}.json"
        if path not in folder_files:
            folder_files[path] = []
        folder_files[path].append(filename)

        serializer = NodeSerializer(node)
        sync_file(project, f"{path}/{filename}", serializer.data)

    for path, files in folder_files.items():
        cleanup_files(project, path, files)


@shared_task
def sync_node(key, token=None):
    project = get_project(token)
    node = get_object_or_404(Node, pk=key)
    path = f"nodes/{node.nodetype.folder}"
    serializer = NodeSerializer(node)
    sync_file(project, f"{path}/{node.key}.json", serializer.data)


@shared_task
def delete_node(key, folder, source_nodes, token=None):
    project = get_project(token)
    path = f"nodes/{folder}"
    delete_file(project, path, f"{key}.json")

    # update related nodes which has edges to the node
    for nodekey in source_nodes:
        sync_node(nodekey, token)


def sync_lists(token=None):
    project = get_project(token)
    files = []
    for li in List.objects.all():
        files.append(li.key + ".json")
        serializer = ListSerializer(li)
        sync_file(project, f"lists/{li.key}.json", serializer.data)
    cleanup_files(project, "lists", files)


@shared_task
def sync_list(key, token=None):
    project = get_project(token)
    serializer = ListSerializer(get_object_or_404(List, pk=key))
    sync_file(project, f"lists/{key}.json", serializer.data)


@shared_task
def delete_list(key, token=None):
    project = get_project(token)
    delete_file(project, "lists", f"{key}.json")


def sync_graphs(token=None):
    project = get_project(token)
    files = []
    for graph in Graph.objects.all():
        files.append(graph.key + ".json")
        serializer = GraphSerializer(graph)
        sync_file(project, f"graphs/{graph.key}.json", serializer.data)
    cleanup_files(project, "graphs", files)


@shared_task
def sync_graph(key, token=None):
    project = get_project(token)
    serializer = GraphSerializer(get_object_or_404(Graph, pk=key))
    sync_file(project, f"graphs/{key}.json", serializer.data)


@shared_task
def delete_graph(key, token=None):
    project = get_project(token)
    delete_file(project, "graphs", f"{key}.json")


@shared_task
def sync_to_gitlab_task():
    print("start to sync data to gitlab..")
    sync_schemas()
    sync_nodetypes()
    sync_edgetypes()
    sync_nodes()
    sync_lists()
    sync_graphs()
    print("sync data to gitlab finished..")
