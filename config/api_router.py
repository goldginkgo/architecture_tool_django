from django.conf import settings
from rest_framework.routers import DefaultRouter, SimpleRouter

from architecture_tool_django.modeling.api.views import (
    EdgetypeViewSet,
    NodetypeViewSet,
    SchemaViewSet,
)

# from architecture_tool_django.users.api.views import UserViewSet

if settings.DEBUG:
    router = DefaultRouter()
else:
    router = SimpleRouter()

# router.register("users", UserViewSet)
router.register("schemas", SchemaViewSet)
router.register("nodetypes", NodetypeViewSet)
router.register("edgetypes", EdgetypeViewSet)

app_name = "api"
urlpatterns = router.urls
