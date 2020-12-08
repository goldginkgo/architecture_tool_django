import json
import logging
import os
import tempfile
from shutil import make_archive, unpack_archive

from celery import shared_task
from django.core.files import File
from django.core.files.storage import default_storage
from django.db.models import Q
from django.shortcuts import get_object_or_404

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

from . import gitlab_utils

logger = logging.getLogger(__name__)


def sync_schemas(token=None):
    project = gitlab_utils.get_project(token)
    files = []
    for schema in Schema.objects.all():
        files.append(schema.key + ".json")
        serializer = SchemaSerializer(schema)
        gitlab_utils.sync_file(
            project, f"modeling/schemas/{schema.key}.json", serializer.data
        )
    gitlab_utils.cleanup_files(project, "modeling/schemas", files)


@shared_task
def sync_schema(key, token=None):
    project = gitlab_utils.get_project(token)
    serializer = SchemaSerializer(get_object_or_404(Schema, pk=key))
    gitlab_utils.sync_file(project, f"modeling/schemas/{key}.json", serializer.data)


@shared_task
def delete_schema(key, token=None):
    project = gitlab_utils.get_project(token)
    gitlab_utils.delete_file(project, "modeling/schemas", f"{key}.json")
    # ensure related nodetypes/edgetypes/nodes/lists/graphs are deleted
    sync_nodetypes()
    sync_edgetypes()
    cleanup_nodes()
    cleanup_lists()
    cleanup_graphs()


@shared_task
def sync_nodetypes(token=None):
    project = gitlab_utils.get_project(token)
    serializer = NodetypeSerializer(Nodetype.objects.all(), many=True)
    gitlab_utils.sync_file(project, "modeling/nodetypes.json", serializer.data)


@shared_task
def delete_nodetype(token=None):
    project = gitlab_utils.get_project(token)
    serializer = NodetypeSerializer(Nodetype.objects.all(), many=True)
    gitlab_utils.sync_file(project, "modeling/nodetypes.json", serializer.data)
    # ensure related edgetypes/nodes are deleted
    sync_edgetypes()
    cleanup_nodes()


@shared_task
def sync_edgetypes(token=None):
    project = gitlab_utils.get_project(token)
    serializer = EdgetypeSerializer(Edgetype.objects.all(), many=True)
    gitlab_utils.sync_file(project, "modeling/edgetypes.json", serializer.data)


@shared_task
def delete_edgetype(token=None):
    project = gitlab_utils.get_project(token)
    serializer = EdgetypeSerializer(Edgetype.objects.all(), many=True)
    gitlab_utils.sync_file(project, "modeling/edgetypes.json", serializer.data)
    # ensure related nodes are updated
    sync_nodes()


def sync_nodes(token=None):
    project = gitlab_utils.get_project(token)
    for node in Node.objects.all():
        path = f"nodes/{node.nodetype.folder}"
        filename = f"{node.key}.json"
        serializer = NodeSerializer(node)
        gitlab_utils.sync_file(project, f"{path}/{filename}", serializer.data)

    cleanup_nodes()


def cleanup_nodes(token=None):
    project = gitlab_utils.get_project(token)
    folder_files = {}
    for node in Node.objects.all():
        path = f"nodes/{node.nodetype.folder}"
        filename = f"{node.key}.json"
        if path not in folder_files:
            folder_files[path] = []
        folder_files[path].append(filename)

    # cleanup non-existing nodes
    for folder in project.repository_tree("nodes", all=True):
        path = f"nodes/{folder['name']}"
        if path in list(folder_files):
            gitlab_utils.cleanup_files(project, path, folder_files[path])
        else:
            for item in project.repository_tree(path, all=True):
                gitlab_utils.delete_file(project, path, item["name"])


@shared_task
def sync_node(key, token=None):
    project = gitlab_utils.get_project(token)
    node = get_object_or_404(Node, pk=key)
    path = f"nodes/{node.nodetype.folder}"
    serializer = NodeSerializer(node)
    gitlab_utils.sync_file(project, f"{path}/{node.key}.json", serializer.data)


@shared_task
def delete_node(key, folder, source_nodes, token=None):
    project = gitlab_utils.get_project(token)
    path = f"nodes/{folder}"
    gitlab_utils.delete_file(project, path, f"{key}.json")

    # update related nodes which has edges to the node
    for nodekey in source_nodes:
        sync_node(nodekey, token)


def sync_lists(token=None):
    project = gitlab_utils.get_project(token)
    files = []
    for li in List.objects.all():
        files.append(li.key + ".json")
        serializer = ListSerializer(li)
        gitlab_utils.sync_file(project, f"lists/{li.key}.json", serializer.data)
    gitlab_utils.cleanup_files(project, "lists", files)


def cleanup_lists(token=None):
    project = gitlab_utils.get_project(token)
    files = []
    for li in List.objects.all():
        files.append(li.key + ".json")
    gitlab_utils.cleanup_files(project, "lists", files)


@shared_task
def sync_list(key, token=None):
    project = gitlab_utils.get_project(token)
    serializer = ListSerializer(get_object_or_404(List, pk=key))
    gitlab_utils.sync_file(project, f"lists/{key}.json", serializer.data)


@shared_task
def delete_list(key, token=None):
    project = gitlab_utils.get_project(token)
    gitlab_utils.delete_file(project, "lists", f"{key}.json")


def sync_graphs(token=None):
    project = gitlab_utils.get_project(token)
    files = []
    for graph in Graph.objects.all():
        files.append(graph.key + ".json")
        serializer = GraphSerializer(graph)
        gitlab_utils.sync_file(project, f"graphs/{graph.key}.json", serializer.data)
    gitlab_utils.cleanup_files(project, "graphs", files)


def cleanup_graphs(token=None):
    project = gitlab_utils.get_project(token)
    files = []
    for graph in Graph.objects.all():
        files.append(graph.key + ".json")
    gitlab_utils.cleanup_files(project, "graphs", files)


@shared_task
def sync_graph(key, token=None):
    project = gitlab_utils.get_project(token)
    serializer = GraphSerializer(get_object_or_404(Graph, pk=key))
    gitlab_utils.sync_file(project, f"graphs/{key}.json", serializer.data)


@shared_task
def delete_graph(key, token=None):
    project = gitlab_utils.get_project(token)
    gitlab_utils.delete_file(project, "graphs", f"{key}.json")


@shared_task
def sync_to_gitlab_task():
    logger.info("start to sync data to gitlab..")
    sync_schemas()
    sync_nodetypes()
    sync_edgetypes()
    sync_nodes()
    sync_lists()
    sync_graphs()
    logger.info("sync data to gitlab finished..")


def write_file(folder, filename, content):
    filepath = os.path.join(folder, filename)
    new_content = json.dumps(content, indent=2)

    with open(filepath, "w") as file:
        logger.info(f"EXPORT: writing file {filepath}")
        file.write(new_content)


@shared_task
def export_data_task(file_basename):
    logger.info("EXPORT: start to export data..")
    with tempfile.TemporaryDirectory() as tempdir:
        logger.info("EXPORT: Created temporary directory: " + tempdir)
        export_dir = os.path.join(tempdir, "export")

        # schemas
        modeling_folder = os.path.join(export_dir, "modeling")
        schemas_folder = os.path.join(modeling_folder, "schemas")
        os.makedirs(schemas_folder, exist_ok=True)
        for schema in Schema.objects.all():
            serializer = SchemaSerializer(schema)
            write_file(schemas_folder, schema.key + ".json", serializer.data)

        # nodetypes
        serializer = NodetypeSerializer(Nodetype.objects.all(), many=True)
        write_file(modeling_folder, "nodetypes.json", serializer.data)

        # edgetypes
        serializer = EdgetypeSerializer(Edgetype.objects.all(), many=True)
        write_file(modeling_folder, "edgetypes.json", serializer.data)

        # nodes
        nodes_folder = os.path.join(export_dir, "nodes")
        for node in Node.objects.all():
            node_folder = os.path.join(nodes_folder, node.nodetype.folder)
            os.makedirs(node_folder, exist_ok=True)
            serializer = NodeSerializer(node)
            write_file(node_folder, f"{node.key}.json", serializer.data)

        # lists
        lists_folder = os.path.join(export_dir, "lists")
        os.makedirs(lists_folder, exist_ok=True)
        for li in List.objects.all():
            serializer = ListSerializer(li)
            write_file(lists_folder, f"{li.key}.json", serializer.data)

        # graphs
        graphs_folder = os.path.join(export_dir, "graphs")
        os.makedirs(graphs_folder, exist_ok=True)
        for graph in Graph.objects.all():
            serializer = GraphSerializer(graph)
            write_file(graphs_folder, f"{graph.key}.json", serializer.data)

        # archive
        logger.info("EXPORT: Archive exported data.")
        archive_name = os.path.join(tempdir, file_basename)
        make_archive(archive_name, "zip", export_dir)

        # save
        logger.info(
            f"EXPORT: Save exported data to default storage export/{file_basename}.zip"
        )
        default_storage.save(
            f"export/{file_basename}.zip",
            content=File(open(archive_name + ".zip", "rb")),
        )
        logger.info(
            "EXPORT: Check if file exist: "
            + str(default_storage.exists(f"export/{file_basename}.zip"))
        )


@shared_task
def import_data_task(import_file):
    logger.info("IMPORT: start to import data..")

    with tempfile.TemporaryDirectory() as tempdir:
        logger.info("IMPORT: Created temporary directory: " + tempdir)

        filepath = f"import/{import_file}"
        import_file_new = os.path.join(tempdir, import_file)

        if default_storage.exists(filepath):
            with open(import_file_new, "wb+") as dest:
                for chunk in default_storage.open(filepath).chunks():
                    dest.write(chunk)
            logger.info("IMPORT: Unzip import data")
            unpack_archive(import_file_new, tempdir, "zip")

            logger.info("IMPORT: Starting importing resources.")
            import_rescource_folder(
                os.path.join(tempdir, "modeling", "schemas"), "schema"
            )
            import_resource_file(
                os.path.join(tempdir, "modeling", "nodetypes.json"), "nodetype"
            )
            import_resource_file(
                os.path.join(tempdir, "modeling", "edgetypes.json"), "edgetype"
            )
            import_rescource_folder(os.path.join(tempdir, "lists"), "list")
            import_rescource_folder(os.path.join(tempdir, "graphs"), "graph")
            import_nodes(os.path.join(tempdir, "nodes"))
            logger.info("IMPORT: Import is successful.")
        else:
            logger.error("IMPORT: Imported data not exist in storage..")


def import_rescource_folder(folder, rstype):
    for filename in os.listdir(folder):
        filepath = os.path.join(folder, filename)
        with open(filepath, "r") as f:
            data = json.loads(f.read())
            if rstype == "schema":
                serializer = SchemaSerializer(data=data)
            elif rstype == "list":
                serializer = ListSerializer(data=data)
            elif rstype == "graph":
                serializer = GraphSerializer(data=data)
            else:  # node
                data["outbound_edges"] = []
                serializer = NodeSerializer(data=data)

            logger.info(
                f"IMPORT: Importing {filepath}, data valid: {str(serializer.is_valid())}"
            )
            serializer.save()


def import_resource_file(filepath, rstype):
    logger.info(f"IMPORT: import { rstype }..")
    with open(filepath, "r") as f:
        data = json.loads(f.read())
        for rc in data:
            if rstype == "nodetype":
                serializer = NodetypeSerializer(data=rc)
            else:  # "edgetype"
                serializer = EdgetypeSerializer(data=rc)

            logger.info(
                f"IMPORT: Importing {rstype}, JSON: {rc}, data valid: {str(serializer.is_valid())}"
            )
            serializer.save()


def import_nodes(nodes_path):
    # Add nodes without edges
    for nodetype_folder in os.listdir(nodes_path):
        import_rescource_folder(os.path.join(nodes_path, nodetype_folder), "nodes")

    # Add edges for nodes
    logger.info("IMPORT: Adding edges for nodes")
    for nodetype_folder in os.listdir(nodes_path):
        nodetype_path = os.path.join(nodes_path, nodetype_folder)
        for filename in os.listdir(nodetype_path):
            node_path = os.path.join(nodetype_path, filename)
            with open(node_path, "r") as f:
                node = json.loads(f.read())
                instance = get_object_or_404(Node, pk=node["key"])
                for edge in node["outbound_edges"]:
                    target_node = get_object_or_404(Node, pk=edge["target"])
                    edge_type = Edgetype.objects.get(
                        Q(source_nodetype=instance.nodetype)
                        & Q(target_nodetype=target_node.nodetype)
                        & Q(edgetype=edge["edge_type"])
                    )
                    instance.add_edge(target_node, edge_type)
