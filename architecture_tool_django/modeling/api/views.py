from django.utils.decorators import method_decorator
from drf_yasg.utils import swagger_auto_schema
from rest_framework import viewsets

from ..models import Schema
from .serializers import SchemaSerializer


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
        operation_summary="Create a schea",
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
