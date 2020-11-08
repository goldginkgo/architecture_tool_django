from django.conf import settings
from rest_framework.routers import DefaultRouter, SimpleRouter

from architecture_tool_django.graphdefs.api.views import GraphViewSet
from architecture_tool_django.listdefs.api.views import ListViewSet
from architecture_tool_django.modeling.api.views import (
    EdgetypeViewSet,
    NodetypeViewSet,
    SchemaViewSet,
)
from architecture_tool_django.nodes.api.views import NodeViewSet

# from architecture_tool_django.users.api.views import UserViewSet

if settings.DEBUG:
    router = DefaultRouter()
else:
    router = SimpleRouter()

# router.register("users", UserViewSet)
router.register("schemas", SchemaViewSet)
router.register("nodetypes", NodetypeViewSet)
router.register("edgetypes", EdgetypeViewSet)
router.register("nodes", NodeViewSet)
router.register("lists", ListViewSet)
router.register("graphs", GraphViewSet)

app_name = "api"
urlpatterns = router.urls
