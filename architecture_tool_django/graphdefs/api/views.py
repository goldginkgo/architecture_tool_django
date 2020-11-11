from django.conf import settings
from django.db.models import Q
from django.http import HttpResponse
from django.template.loader import get_template
from django.utils.decorators import method_decorator
from drf_yasg.utils import swagger_auto_schema
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny

from architecture_tool_django.nodes.models import Edge, Node

from ..models import Graph
from .serializers import GraphSerializer


@method_decorator(
    name="partial_update", decorator=swagger_auto_schema(auto_schema=None)
)
@method_decorator(
    name="list",
    decorator=swagger_auto_schema(
        tags=["graphs"],
        operation_summary="List all graphs",
    ),
)
@method_decorator(
    name="create",
    decorator=swagger_auto_schema(
        tags=["graphs"],
        operation_summary="Create a graph",
    ),
)
@method_decorator(
    name="retrieve",
    decorator=swagger_auto_schema(
        tags=["graphs"],
        operation_summary="Retrieve a graph",
    ),
)
@method_decorator(
    name="update",
    decorator=swagger_auto_schema(
        tags=["graphs"],
        operation_summary="Update a graph",
    ),
)
@method_decorator(
    name="destroy",
    decorator=swagger_auto_schema(
        tags=["graphs"],
        operation_summary="Destroy a graph",
    ),
)
class GraphViewSet(viewsets.ModelViewSet):
    """
    This is for dealing with node graphs.

    list: List all graphs

    retrieve: Retrieve a graph

    update: Update a graph

    create: Create a graph

    destroy: Destroy a graph
    """

    queryset = Graph.objects.all()
    serializer_class = GraphSerializer

    @action(detail=True, methods=["get"], permission_classes=[AllowAny])
    @swagger_auto_schema(
        tags=["graphs"],
        operation_summary="Get plantuml definition for a graph",
    )
    def plantuml(self, request, pk):
        """
        Get plantuml definition for a graph
        """
        nodes_to_draw = []
        edges_to_draw = []

        obj = Graph.objects.get(key=pk)

        method = obj.graph["nodes"]["filter"]["method"]
        nodetypes = obj.graph["nodes"]["filter"]["types"]
        selection = obj.graph["nodes"]["filter"]["selection"]
        edgetypes = obj.graph["edges"]["filter"]["types"]

        nodetypes_regex = "|".join(nodetypes)
        edgetypes_regex = "|".join(edgetypes)

        if method == "all":
            matched_nodes = list(
                Node.objects.filter(nodetype__key__iregex=nodetypes_regex).values_list(
                    "key", flat=True
                )
            )
            nodes_to_draw = matched_nodes

            edges = Edge.objects.filter(
                Q(edge_type__edgetype__iregex=edgetypes_regex)
                & Q(source__key__in=matched_nodes)
                & Q(target__key__in=matched_nodes)
            )

            for edge in edges:
                source = edge.source.key
                target = edge.target.key
                edges_to_draw.append([source, target, edge.edge_type.edgetype])

        elif method == "onlyWithEdges":
            matched_nodes = list(
                Node.objects.filter(nodetype__key__iregex=nodetypes_regex).values_list(
                    "key", flat=True
                )
            )
            edges = Edge.objects.filter(
                Q(edge_type__edgetype__iregex=edgetypes_regex)
                & Q(source__key__in=matched_nodes)
                & Q(target__key__in=matched_nodes)
            )

            for edge in edges:
                source = edge.source.key
                target = edge.target.key
                edges_to_draw.append([source, target, edge.edge_type.edgetype])
                if source not in nodes_to_draw:
                    nodes_to_draw.append(source)
                if target not in nodes_to_draw:
                    nodes_to_draw.append(target)

        elif method == "selection":
            matched_nodes = list(
                Node.objects.filter(
                    nodetype__key__iregex=nodetypes_regex, key__in=selection
                ).values_list("key", flat=True)
            )

            nodes_to_draw = matched_nodes
            edges = Edge.objects.filter(
                Q(edge_type__edgetype__iregex=edgetypes_regex)
                & Q(source__key__in=matched_nodes)
                & Q(target__key__in=matched_nodes)
            )
            for edge in edges:
                source = edge.source.key
                target = edge.target.key

                edges_to_draw.append([source, target, edge.edge_type.edgetype])

        elif method == "selectionWithNeighbors":
            matched_nodes = list(
                Node.objects.filter(
                    nodetype__key__iregex=nodetypes_regex, key__in=selection
                ).values_list("key", flat=True)
            )

            nodes_to_draw = matched_nodes
            edges = Edge.objects.filter(
                Q(edge_type__edgetype__iregex=edgetypes_regex)
                & (Q(source__key__in=matched_nodes) | Q(target__key__in=matched_nodes))
            )
            extra_nodes = []
            for edge in edges:
                source = edge.source.key
                target = edge.target.key

                edges_to_draw.append([source, target, edge.edge_type.edgetype])

                if source not in nodes_to_draw and source not in extra_nodes:
                    extra_nodes.append(source)
                if target not in nodes_to_draw and target not in extra_nodes:
                    extra_nodes.append(target)

            nodes_to_draw += extra_nodes

        elif method == "parents":
            matched_nodes = list(
                Node.objects.filter(
                    nodetype__key__iregex=nodetypes_regex, key__in=selection
                ).values_list("key", flat=True)
            )
            nodes_to_draw.extend(matched_nodes)
            edges = Edge.objects.filter(
                Q(edge_type__edgetype__iregex=edgetypes_regex)
                & Q(source__key__in=matched_nodes)
            )
            while edges.exists():
                new_targets = []
                for edge in edges:
                    source = edge.source.key
                    target = edge.target.key

                    edges_to_draw.append([source, target, edge.edge_type.edgetype])
                    if target not in nodes_to_draw:
                        nodes_to_draw.append(target)
                        new_targets.append(target)
                edges = Edge.objects.filter(
                    Q(edge_type__edgetype__iregex=edgetypes_regex)
                    & Q(source__key__in=new_targets)
                )

        else:
            pass

        node_names = {}
        for node in Node.objects.all():
            node_names[node.key] = node.attributeSet["name"]

        context = {
            "arctool_url": settings.ARCHITECTURE_TOOL_URL,
            "title": obj.graph["title"],
            "nodes_to_draw": nodes_to_draw,
            "edges_to_draw": edges_to_draw,
            "node_names": node_names,
        }
        puml = get_template("misc/graph.puml").render(context)

        return HttpResponse(puml, content_type="text/plain")
