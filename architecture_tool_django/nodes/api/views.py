from django.utils.decorators import method_decorator
from drf_yasg.utils import swagger_auto_schema
from rest_framework import viewsets

from ..models import Node
from .serializers import NodeSerializer


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
