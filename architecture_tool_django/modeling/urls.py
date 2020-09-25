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
    path("schemas/node/", views.node, name="schema.node"),
    path("schemas/list/", views.list, name="schema.list"),
    path("schemas/graph/", views.graph, name="schema.graph"),
]
