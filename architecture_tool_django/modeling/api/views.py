from django.conf import settings
from django.db.models import Q
from django.http import JsonResponse
from django.utils.decorators import method_decorator
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import viewsets
from rest_framework.decorators import action

from architecture_tool_django.common.tasks import (
    delete_edgetype,
    delete_nodetype,
    delete_schema,
    sync_edgetypes,
    sync_nodetypes,
    sync_schema,
)
from architecture_tool_django.utils.utils import log_user_action

from ..models import Edgetype, Nodetype, Schema
from .serializers import EdgetypeSerializer, NodetypeSerializer, SchemaSerializer

q_param = openapi.Parameter(
    "q",
    openapi.IN_QUERY,
    description="The current search term in the search box",
    type=openapi.TYPE_STRING,
)


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

    def perform_create(self, serializer):
        serializer.save()

        key = serializer.initial_data["key"]
        log_user_action(self.request.user, "add", "schema", key)

        if settings.SYNC_TO_GITLAB:
            access_token = self.request.user.get_gitlab_access_token()
            sync_schema.delay(key, access_token)

    def perform_update(self, serializer):
        serializer.save()

        key = serializer.initial_data["key"]
        log_user_action(self.request.user, "update", "schema", key)

        if settings.SYNC_TO_GITLAB:
            access_token = self.request.user.get_gitlab_access_token()
            sync_schema.delay(key, access_token)

    def perform_destroy(self, instance):
        key = instance.key
        instance.delete()

        log_user_action(self.request.user, "delete", "schema", key)

        if settings.SYNC_TO_GITLAB:
            access_token = self.request.user.get_gitlab_access_token()
            delete_schema.delay(key, access_token)


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

    def perform_create(self, serializer):
        serializer.save()

        key = serializer.initial_data["key"]
        log_user_action(self.request.user, "add", "nodetype", key)

        if settings.SYNC_TO_GITLAB:
            access_token = self.request.user.get_gitlab_access_token()
            sync_nodetypes.delay(access_token)

    def perform_update(self, serializer):
        serializer.save()

        key = serializer.initial_data["key"]
        log_user_action(self.request.user, "update", "nodetype", key)

        if settings.SYNC_TO_GITLAB:
            access_token = self.request.user.get_gitlab_access_token()
            sync_nodetypes.delay(access_token)

    def perform_destroy(self, instance):
        key = instance.key
        instance.delete()

        log_user_action(self.request.user, "delete", "nodetype", key)

        if settings.SYNC_TO_GITLAB:
            access_token = self.request.user.get_gitlab_access_token()
            delete_nodetype.delay(access_token)

    @action(detail=False, methods=["get"])
    @swagger_auto_schema(
        tags=["nodetypes"],
        manual_parameters=[q_param],
        operation_summary="Select2 ajax request for getting nodetypes",
    )
    def select2(self, request):
        """
        Select2 ajax request for getting nodetypes
        """
        if request.GET.get("q"):
            nodetypes = Nodetype.objects.filter(name__iregex=request.GET.get("q"))
        else:
            nodetypes = Nodetype.objects.all()

        ret = {"results": []}
        for nodetype in nodetypes:
            ret["results"].append({"id": nodetype.key, "text": nodetype.name})

        return JsonResponse(ret)

    @action(detail=True, methods=["get"])
    @swagger_auto_schema(
        tags=["nodetypes"],
        operation_summary="Select2 ajax request for getting outgoing edgetypes for a nodetype",
    )
    def edgetypes(self, request, pk):
        """
        Ajax request for getting existing edgetype in select for node
        """
        q = request.GET.get("q")

        if q:
            edgetypes = Edgetype.objects.filter(
                Q(source_nodetype__key=pk) & Q(edgetype_name__iregex=q)
            )
        else:
            edgetypes = Edgetype.objects.filter(source_nodetype__key=pk)

        ret = {"results": []}
        for edgetype in edgetypes:
            text = f"{edgetype.edgetype} -> [{edgetype.target_nodetype.key}]"
            ret["results"].append(
                {"id": edgetype.id, "text": text, "edge_type": edgetype.edgetype}
            )

        return JsonResponse(ret)


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

    def perform_create(self, serializer):
        serializer.save()

        log_user_action(self.request.user, "add", "edgetype", "")

        if settings.SYNC_TO_GITLAB:
            access_token = self.request.user.get_gitlab_access_token()
            sync_edgetypes.delay(access_token)

    def perform_update(self, serializer):
        serializer.save()

        log_user_action(self.request.user, "update", "edgetype", "")

        if settings.SYNC_TO_GITLAB:
            access_token = self.request.user.get_gitlab_access_token()
            sync_edgetypes.delay(access_token)

    def perform_destroy(self, instance):
        instance.delete()

        log_user_action(self.request.user, "delete", "edgetype", "")

        if settings.SYNC_TO_GITLAB:
            access_token = self.request.user.get_gitlab_access_token()
            delete_edgetype.delay(access_token)

    @action(detail=True, methods=["get"])
    @swagger_auto_schema(
        tags=["edgetypes"],
        operation_summary="Ajax request for getting existing edgetype in select for node",
    )
    def select(self, request, pk):
        """
        Ajax request for getting existing edgetype in select for node
        """
        edgetype = Edgetype.objects.get(id=pk)
        text = f"{edgetype.edgetype} -> [{edgetype.target_nodetype.key}]"
        return JsonResponse(
            {"id": edgetype.id, "text": text, "edge_type": edgetype.edgetype}
        )
