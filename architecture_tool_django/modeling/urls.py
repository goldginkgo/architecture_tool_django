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
    path("ajax/nodetypes/", views.get_nodetypes_ajax, name="ajax.nodetypes"),
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
    path("edgetypes/", views.EdgeTypeListView.as_view(), name="edgetype.list"),
    path(
        "edgetypes/create/", views.EdgeTypeCreateView.as_view(), name="edgetype.create"
    ),
    path(
        "edgetypes/<str:pk>/",
        views.EdgeTypeDetailView.as_view(),
        name="edgetype.detail",
    ),
    path(
        "edgetypes/<str:pk>/update/",
        views.EdgeTypeUpdateView.as_view(),
        name="edgetype.update",
    ),
    path(
        "edgetypes/<str:pk>/delete/",
        views.EdgeTypeDeleteView.as_view(),
        name="edgetype.delete",
    ),
    path("ajax/edgetypes/", views.get_edgetypes_ajax, name="ajax.edgetypes"),
    path(
        "ajax/edgetypes/<str:pk>/", views.get_edgetype_ajax, name="ajax.edgetype.detail"
    ),
]
