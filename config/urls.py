from django.conf import settings
from django.conf.urls import url
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path
from django.views import defaults as default_views
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from drf_yasg.views import get_schema_view
from rest_framework import permissions
from rest_framework.authtoken.serializers import AuthTokenSerializer
from rest_framework.authtoken.views import obtain_auth_token

schema_view = get_schema_view(
    openapi.Info(
        title="Architecture Tool",
        default_version="v1",
        description="""APIs for Architecture Tool.

The `swagger-ui` view can be found [here](/swagger/).
The swagger YAML document can be found [here](/swagger.yaml).

(Remember to add the "Token" prefix when adding DRF token to swagger-ui.)""",  # noqa,
        terms_of_service="",
        contact=openapi.Contact(email="emailtest@gmail.com"),
        license=openapi.License(name="MIT License"),
    ),
    public=False,
    permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    url(
        r"^swagger(?P<format>\.json|\.yaml)$",
        schema_view.without_ui(cache_timeout=0),
        name="schema-json",
    ),
    url(
        r"^swagger/$",
        schema_view.with_ui("swagger", cache_timeout=0),
        name="schema-swagger-ui",
    ),
    # url(r'^redoc/$', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
    # Django Admin, use {% url 'admin:index' %}
    path(settings.ADMIN_URL, admin.site.urls),
    # User management
    path("users/", include("architecture_tool_django.users.urls", namespace="users")),
    path("accounts/", include("allauth.urls")),
    # Your stuff: custom urls includes go here
    path("", include("architecture_tool_django.dashboard.urls")),
    path("", include("architecture_tool_django.common.urls")),
    path(
        "modeling/",
        include("architecture_tool_django.modeling.urls", namespace="modeling"),
    ),
    path("", include("architecture_tool_django.nodes.urls", namespace="nodes")),
    path("", include("architecture_tool_django.listdefs.urls", namespace="lists")),
    path("", include("architecture_tool_django.graphdefs.urls", namespace="graphs")),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# TODO support token expiration
decorated_auth_view = swagger_auto_schema(
    method="post", request_body=AuthTokenSerializer
)(obtain_auth_token)

# API URLS
urlpatterns += [
    # API base url
    path("api/", include("config.api_router")),
    # DRF auth token
    path("auth-token/", decorated_auth_view),
]

if settings.DEBUG:
    # This allows the error pages to be debugged during development, just visit
    # these url in browser to see how these error pages look like.
    urlpatterns += [
        path(
            "400/",
            default_views.bad_request,
            kwargs={"exception": Exception("Bad Request!")},
        ),
        path(
            "403/",
            default_views.permission_denied,
            kwargs={"exception": Exception("Permission Denied")},
        ),
        path(
            "404/",
            default_views.page_not_found,
            kwargs={"exception": Exception("Page not Found")},
        ),
        path("500/", default_views.server_error),
    ]
    if "debug_toolbar" in settings.INSTALLED_APPS:
        import debug_toolbar

        urlpatterns = [path("__debug__/", include(debug_toolbar.urls))] + urlpatterns
