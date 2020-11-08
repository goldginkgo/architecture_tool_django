from django.utils.decorators import method_decorator
from drf_yasg.utils import swagger_auto_schema
from rest_framework import viewsets

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
