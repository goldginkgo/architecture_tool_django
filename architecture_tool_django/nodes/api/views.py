from django.conf import settings
from django.http import HttpResponse, JsonResponse
from django.utils.decorators import method_decorator
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny

from architecture_tool_django.modeling.models import Edgetype

from ..models import Node
from .serializers import NodeSerializer

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


@method_decorator(
    name="partial_update", decorator=swagger_auto_schema(auto_schema=None)
)
@method_decorator(
    name="list",
    decorator=swagger_auto_schema(
        tags=["nodes"],
        operation_summary="List all resources",
    ),
)
@method_decorator(
    name="create",
    decorator=swagger_auto_schema(
        tags=["nodes"],
        operation_summary="Create a new resource",
    ),
)
@method_decorator(
    name="retrieve",
    decorator=swagger_auto_schema(
        tags=["nodes"],
        operation_summary="Retrieve a Resource",
    ),
)
@method_decorator(
    name="update",
    decorator=swagger_auto_schema(
        tags=["nodes"],
        operation_summary="Update a resource",
    ),
)
@method_decorator(
    name="destroy",
    decorator=swagger_auto_schema(
        tags=["nodes"],
        operation_summary="Destroy a resource",
    ),
)
class NodeViewSet(viewsets.ModelViewSet):
    """
    This is for dealing with nodes.

    list: List all resources

    retrieve: Retrieve a Resource

    update: Update a resource

    create: Create something

    destroy: Destroy a resource
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

    def create_puml_definition(self, title, nodes_to_draw, edges_to_draw):
        arctool_url = settings.ARCHITECTURE_TOOL_URL
        t = f"{arctool_url}/static/plugins/puml-themes/puml-theme-cerulean.puml\n"

        puml = ""
        puml += "@startuml\n"
        puml += f"!include {t}"
        puml += "left to right direction\n"
        puml += "skinparam componentStyle uml2\n"
        puml += "skinparam titleBorderRoundCorner 15\n"
        puml += "skinparam titleBorderThickness 2\n"

        puml += "skinparam component {\n"
        puml += "FontSize 12\n"
        puml += "}\n"
        puml += "skinparam actor {\n"
        puml += "FontSize 12\n"
        puml += "}\n"
        puml += "skinparam package {\n"
        puml += "FontSize 12\n"
        puml += "}\n"

        puml += f"title {title}\n"
        for node in nodes_to_draw:
            name = Node.objects.get(key=node).attributeSet["name"]
            puml = (
                puml
                + f"[({node}) {name}] as {node.replace('-', '_')} [[{settings.ARCHITECTURE_TOOL_URL}/nodes/{node}]]\n"
            )

        # TODO colorize components

        for edge in edges_to_draw:
            puml = (
                puml
                + edge[0].replace("-", "_")
                + " --> "
                + edge[1].replace("-", "_")
                + " : "
                + edge[2]
                + "\n"
            )
        puml += "@enduml"
        print(puml)
        return puml

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

        neighbor_puml = self.create_puml_definition(
            "Node Neighbors", nodes_to_draw, edges_to_draw
        )
        return HttpResponse(neighbor_puml, content_type="text/plain")
