from django.utils.decorators import method_decorator
from drf_yasg.utils import swagger_auto_schema
from rest_framework import viewsets

from ..models import List
from .serializers import ListSerializer


@method_decorator(
    name="partial_update", decorator=swagger_auto_schema(auto_schema=None)
)
@method_decorator(
    name="list",
    decorator=swagger_auto_schema(
        tags=["lists"],
        operation_summary="List all lists",
    ),
)
@method_decorator(
    name="create",
    decorator=swagger_auto_schema(
        tags=["lists"],
        operation_summary="Create a list",
    ),
)
@method_decorator(
    name="retrieve",
    decorator=swagger_auto_schema(
        tags=["lists"],
        operation_summary="Retrieve a list",
    ),
)
@method_decorator(
    name="update",
    decorator=swagger_auto_schema(
        tags=["lists"],
        operation_summary="Update a list",
    ),
)
@method_decorator(
    name="destroy",
    decorator=swagger_auto_schema(
        tags=["lists"],
        operation_summary="Destroy a list",
    ),
)
class ListViewSet(viewsets.ModelViewSet):
    """
    This is for dealing with node lists.

    list: List all lists

    retrieve: Retrieve a list

    update: Update a list

    create: Create a list

    destroy: Destroy a list
    """

    queryset = List.objects.all()
    serializer_class = ListSerializer
