import logging

from django.conf import settings
from django.http import HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404
from django.template.loader import get_template
from django.utils.decorators import method_decorator
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny

from architecture_tool_django.common.tasks import delete_node, sync_node, sync_nodes
from architecture_tool_django.modeling.models import Edgetype
from architecture_tool_django.utils.utils import log_user_action

from ..models import Node
from .serializers import NodeSerializer

logger = logging.getLogger(__name__)

q_param = openapi.Parameter(
    "q",
    openapi.IN_QUERY,
    description="The current search term in the search box",
    type=openapi.TYPE_STRING,
)

edgetype_id_param = openapi.Parameter(
    "edgetype_id",
    openapi.IN_QUERY,
    description="Selected edgetype id",
    type=openapi.TYPE_STRING,
)

rename_body = openapi.Schema(
    type=openapi.TYPE_OBJECT,
    properties={
        "from": openapi.Schema(
            type=openapi.TYPE_STRING, description="The original node key"
        ),
        "to": openapi.Schema(
            type=openapi.TYPE_STRING, description="The expected node key"
        ),
    },
)


@method_decorator(
    name="partial_update", decorator=swagger_auto_schema(auto_schema=None)
)
@method_decorator(
    name="list",
    decorator=swagger_auto_schema(
        tags=["nodes"],
        operation_summary="List all nodes",
    ),
)
@method_decorator(
    name="create",
    decorator=swagger_auto_schema(
        tags=["nodes"],
        operation_summary="Create a new node",
    ),
)
@method_decorator(
    name="retrieve",
    decorator=swagger_auto_schema(
        tags=["nodes"],
        operation_summary="Retrieve a node",
    ),
)
@method_decorator(
    name="update",
    decorator=swagger_auto_schema(
        tags=["nodes"],
        operation_summary="Update a node",
    ),
)
@method_decorator(
    name="destroy",
    decorator=swagger_auto_schema(
        tags=["nodes"],
        operation_summary="Destroy a node",
    ),
)
class NodeViewSet(viewsets.ModelViewSet):
    """
    This is for dealing with nodes.

    list: List all nodes

    retrieve: Retrieve a node

    update: Update a node

    create: Create a new node

    destroy: Destroy a node
    """

    lookup_value_regex = r"[\w.-]+"
    queryset = Node.objects.all()
    serializer_class = NodeSerializer

    @action(detail=False, methods=["get"])
    @swagger_auto_schema(
        tags=["nodes"],
        manual_parameters=[q_param, edgetype_id_param],
        operation_summary="Select2 ajax request for getting outbound nodes for a edgetype",
    )
    def targetnodes(self, request):
        """
        Select2 ajax request for getting outbound nodes for a edgetype
        """
        ret = {"results": []}

        q = request.GET.get("q")
        edgetype_id = request.GET.get("edgetype_id")

        if edgetype_id:
            edgetype = Edgetype.objects.get(pk=edgetype_id)
            nodes = edgetype.target_nodetype.nodes
            if q:
                nodes = nodes.filter(pk__iregex=q)

            for node in nodes.all():
                ret["results"].append({"id": node.key, "text": str(node)})

        return JsonResponse(ret)

    @action(detail=True, methods=["get"])
    @swagger_auto_schema(
        tags=["nodes"],
        operation_summary="Ajax request to get a node by node key for select2 option",
    )
    def targetnode(self, request, pk):
        """
        Ajax request to get a node by node key for select2 option
        """
        node = Node.objects.get(key=pk)
        return JsonResponse({"id": pk, "text": str(node)})

    @action(detail=True, methods=["get"], permission_classes=[AllowAny])
    @swagger_auto_schema(
        tags=["nodes"],
        operation_summary="Get plantuml definition for a node",
    )
    def plantuml(self, request, pk):
        """
        Get plantuml definition for a node
        """
        node = Node.objects.get(key=pk)

        nodes_to_draw = [node.key]

        target_nodes = list(node.target_nodes.all().values_list("key", flat=True))
        nodes_to_draw.extend(target_nodes)

        source_nodes = list(node.source_nodes.all().values_list("key", flat=True))
        nodes_to_draw.extend(source_nodes)

        # uniq nodes
        nodes_to_draw = list(set(nodes_to_draw))

        edges_to_draw = []
        for edge in node.outbound_edges.all():
            edges_to_draw.append([node.key, edge.target.key, edge.edge_type.edgetype])
        for edge in node.inbound_edges.all():
            edges_to_draw.append([edge.source.key, node.key, edge.edge_type.edgetype])

        node_names = {}
        for node in Node.objects.all():
            node_names[node.key] = node.attributeSet["name"]

        context = {
            "arctool_url": settings.ARCHITECTURE_TOOL_URL,
            "title": "Node Neighbors",
            "nodes_to_draw": nodes_to_draw,
            "edges_to_draw": edges_to_draw,
            "node_names": node_names,
        }
        puml = get_template("misc/graph.puml").render(context)

        puml = "\n".join([i.rstrip() for i in puml.splitlines() if i.strip()])
        return HttpResponse(puml, content_type="text/plain")

    @action(detail=False, methods=["post"])
    @swagger_auto_schema(
        tags=["nodes"],
        request_body=rename_body,
        operation_summary="Rename individual node key",
    )
    def rename(self, request):
        """
        Rename individual node key. (Add new node, update related nodes, delete old node)
        """
        logger.info("Renaming node key..")
        logger.info(request.data)

        node = get_object_or_404(Node, pk=request.data.get("from"))
        node_data = NodeSerializer(node).data
        node_data["key"] = request.data.get("to")
        serializer = NodeSerializer(data=node_data)
        if serializer.is_valid():
            # TODO should be a transaction for followig operations
            new_node = serializer.save()

            for edge in node.inbound_edges.all():
                edge.source.add_edge(new_node, edge.edge_type)

            node.delete()

            log_user_action(
                self.request.user, "rename", "node", request.data.get("from")
            )

            if settings.SYNC_TO_GITLAB:
                access_token = self.request.user.get_gitlab_access_token()
                sync_nodes.delay(access_token)

            return JsonResponse({"detail": "successfully renamed node"})
        else:
            return JsonResponse(
                {"detail": "request body not valid"}, status=status.HTTP_400_BAD_REQUEST
            )

    def perform_create(self, serializer):
        serializer.save()

        key = serializer.initial_data["key"]
        log_user_action(self.request.user, "add", "node", key)

        if settings.SYNC_TO_GITLAB:
            access_token = self.request.user.get_gitlab_access_token()
            sync_node.delay(key, access_token)

    def perform_update(self, serializer):
        serializer.save()

        key = serializer.initial_data["key"]
        log_user_action(self.request.user, "update", "node", key)

        if settings.SYNC_TO_GITLAB:
            access_token = self.request.user.get_gitlab_access_token()
            sync_node.delay(key, access_token)

    def perform_destroy(self, instance):
        key = instance.key
        folder = instance.nodetype.folder
        source_nodes = list(instance.source_nodes.all().values_list("key", flat=True))
        instance.delete()

        log_user_action(self.request.user, "delete", "node", key)

        if settings.SYNC_TO_GITLAB:
            access_token = self.request.user.get_gitlab_access_token()
            delete_node.delay(key, folder, source_nodes, access_token)
