from django.utils.decorators import method_decorator
from drf_yasg.utils import swagger_auto_schema
from rest_framework import viewsets

from ..models import Edgetype, Nodetype, Schema
from .serializers import EdgetypeSerializer, NodetypeSerializer, SchemaSerializer


@swagger_auto_schema(tags=["testtag"])
@method_decorator(
    name="partial_update", decorator=swagger_auto_schema(auto_schema=None)
)
@method_decorator(
    name="list",
    decorator=swagger_auto_schema(
        tags=["schemas"],
        operation_summary="List all schemas",
    ),
)
@method_decorator(
    name="create",
    decorator=swagger_auto_schema(
        tags=["schemas"],
        operation_summary="Create a schema",
    ),
)
@method_decorator(
    name="retrieve",
    decorator=swagger_auto_schema(
        tags=["schemas"],
        operation_summary="Retrieve a schema",
    ),
)
@method_decorator(
    name="update",
    decorator=swagger_auto_schema(
        tags=["schemas"],
        operation_summary="Update a schema",
    ),
)
@method_decorator(
    name="destroy",
    decorator=swagger_auto_schema(
        tags=["schemas"],
        operation_summary="Delete a schema",
    ),
)
class SchemaViewSet(viewsets.ModelViewSet):
    """
    This is for dealing with schemas.

    list: List all schemas

    retrieve: Retrieve a schema

    update: Update a schema

    create: Create a schema

    destroy: Destroy a schema
    """

    queryset = Schema.objects.all()
    serializer_class = SchemaSerializer


@method_decorator(
    name="partial_update", decorator=swagger_auto_schema(auto_schema=None)
)
@method_decorator(
    name="list",
    decorator=swagger_auto_schema(
        tags=["nodetypes"],
        operation_summary="List all nodetypes",
    ),
)
@method_decorator(
    name="create",
    decorator=swagger_auto_schema(
        tags=["nodetypes"],
        operation_summary="Create a nodetype",
    ),
)
@method_decorator(
    name="retrieve",
    decorator=swagger_auto_schema(
        tags=["nodetypes"],
        operation_summary="Retrieve a nodetype",
    ),
)
@method_decorator(
    name="update",
    decorator=swagger_auto_schema(
        tags=["nodetypes"],
        operation_summary="Update a nodetype",
    ),
)
@method_decorator(
    name="destroy",
    decorator=swagger_auto_schema(
        tags=["nodetypes"],
        operation_summary="Destroy a nodetype",
    ),
)
class NodetypeViewSet(viewsets.ModelViewSet):
    """
    This is for dealing with nodetypes.

    list: List all nodetypes

    retrieve: Retrieve a nodetype

    update: Update a nodetype

    create: Create a nodetype

    destroy: Destroy a nodetype
    """

    queryset = Nodetype.objects.all()
    serializer_class = NodetypeSerializer


@method_decorator(
    name="partial_update", decorator=swagger_auto_schema(auto_schema=None)
)
@method_decorator(
    name="list",
    decorator=swagger_auto_schema(
        tags=["edgetypes"],
        operation_summary="List all edgetypes",
    ),
)
@method_decorator(
    name="create",
    decorator=swagger_auto_schema(
        tags=["edgetypes"],
        operation_summary="Create a edgetype",
    ),
)
@method_decorator(
    name="retrieve",
    decorator=swagger_auto_schema(
        tags=["edgetypes"],
        operation_summary="Retrieve a edgetype",
    ),
)
@method_decorator(
    name="update",
    decorator=swagger_auto_schema(
        tags=["edgetypes"],
        operation_summary="Update a edgetype",
    ),
)
@method_decorator(
    name="destroy",
    decorator=swagger_auto_schema(
        tags=["edgetypes"],
        operation_summary="Destroy a edgetype",
    ),
)
class EdgetypeViewSet(viewsets.ModelViewSet):
    """
    This is for dealing with edgetypes.

    list: List all edgetypes

    retrieve: Retrieve a edgetype

    update: Update a edgetype

    create: Create a edgetype

    destroy: Destroy a edgetype
    """

    queryset = Edgetype.objects.all()
    serializer_class = EdgetypeSerializer

    def validate(self, data):
        # TODO validate the uniqness of the edgetype

        return data
