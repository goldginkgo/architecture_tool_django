import json

import gitlab
from celery import shared_task
from django.conf import settings
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

GITLAB_TOKEN = settings.GITLAB_TOKEN
GITLAB_PROJECT_ID = settings.GITLAB_PROJECT_ID

gl = gitlab.Gitlab(settings.GITLAB_URL, oauth_token=GITLAB_TOKEN)

project = gl.projects.get(GITLAB_PROJECT_ID)


def ordered(obj):  # compare json
    if isinstance(obj, dict):
        return sorted((k, ordered(v)) for k, v in obj.items())
    if isinstance(obj, list):
        return sorted(ordered(x) for x in obj)
    else:
        return obj


def sync_file(filepath, new_content_json):
    new_content = json.dumps(new_content_json, indent=2)
    try:
        f = project.files.get(file_path=filepath, ref="master")
        old_content = json.loads(f.decode())
        json.loads(f.decode())

        if ordered(old_content) == ordered(new_content_json):
            print(f"{filepath} is update to date.")
        else:
            print(f"sync {filepath} to gitlab..")
            f.content = new_content
            f.save(branch="master", commit_message=f"sync {filepath} to gitlab..")
    except GitlabGetError:
        print(f"sync {filepath} to gitlab..")
        project.files.create(
            {
                "file_path": filepath,
                "branch": "master",
                "content": new_content,
                "commit_message": f"sync {filepath} to gitlab..",
            }
        )


def cleanup_files(path, allowed_files):
    for item in project.repository_tree(path, all=True):
        filename = item["name"]
        if filename not in allowed_files:
            print(f"cleanup {path}/{filename}")
            project.files.delete(
                file_path=f"{path}/{filename}",
                commit_message=f"cleanup {path}/{filename}",
                branch="master",
            )


def sync_schemas():
    files = []
    for schema in Schema.objects.all():
        files.append(schema.key + ".json")
        serializer = SchemaSerializer(schema)
        sync_file(f"modeling/schemas/{schema.key}.json", serializer.data)
    cleanup_files("modeling/schemas", files)


def sync_nodetypes():
    serializer = NodetypeSerializer(Nodetype.objects.all(), many=True)
    sync_file("modeling/nodetypes.json", serializer.data)


def sync_edgetypes():
    serializer = EdgetypeSerializer(Edgetype.objects.all(), many=True)
    sync_file("modeling/edgetypes.json", serializer.data)


def sync_nodes():
    folder_files = {}
    for node in Node.objects.all():
        path = f"nodes/{node.nodetype.folder}"
        filename = f"{node.key}.json"
        if path not in folder_files:
            folder_files[path] = []
        folder_files[path].append(filename)

        serializer = NodeSerializer(node)
        sync_file(f"{path}/{filename}", serializer.data)

    for path, files in folder_files.items():
        cleanup_files(path, files)


def sync_lists():
    files = []
    for li in List.objects.all():
        files.append(li.key + ".json")
        serializer = ListSerializer(li)
        sync_file(f"lists/{li.key}.json", serializer.data)
    cleanup_files("lists", files)


def sync_graphs():
    files = []
    for graph in Graph.objects.all():
        files.append(graph.key + ".json")
        serializer = GraphSerializer(graph)
        sync_file(f"graphs/{graph.key}.json", serializer.data)
    cleanup_files("graphs", files)


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
