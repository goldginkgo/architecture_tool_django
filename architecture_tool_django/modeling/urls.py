from django.urls import path

from . import views

app_name = "modeling"
urlpatterns = [
    path("nodetypes/", views.NodeTypeListView.as_view(), name="nodetype.list"),
    path(
        "nodetypes/create/", views.NodeTypeCreateView.as_view(), name="nodetype.create"
    ),
    path(
        "nodetypes/<str:pk>/",
        views.NodeTypeDetailView.as_view(),
        name="nodetype.detail",
    ),
    path(
        "nodetypes/<str:pk>/update/",
        views.NodeTypeUpdateView.as_view(),
        name="nodetype.update",
    ),
    path(
        "nodetypes/<str:pk>/delete/",
        views.NodeTypeDeleteView.as_view(),
        name="nodetype.delete",
    ),
    path("edgetypes/", views.EdgeTypeListView.as_view(), name="edgetype.list"),
    path("schemas/", views.SchemaListView.as_view(), name="schema.list"),
    path("schemas/create/", views.SchemaCreateView.as_view(), name="schema.create"),
    path(
        "schemas/<str:pk>/",
        views.SchemaDetailView.as_view(),
        name="schema.detail",
    ),
    path(
        "schemas/<str:pk>/update/",
        views.SchemaUpdateView.as_view(),
        name="schema.update",
    ),
    path(
        "schemas/<str:pk>/delete/",
        views.SchemaDeleteView.as_view(),
        name="schema.delete",
    ),
    path("schemaapi/<str:pk>/", views.get_schema, name="schemaapi"),
]
