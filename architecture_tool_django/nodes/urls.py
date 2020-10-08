from django.urls import path

from architecture_tool_django.nodes import views

app_name = "nodes"
urlpatterns = [
    path("node_counts/", views.node_counts, name="node_counts"),
    path("nodeapi/<str:pk>/", views.get_node, name="nodeapi"),
    path("nodes/", views.NodeListView.as_view(), name="node.list"),
    path("nodes/create/", views.NodeCreateView.as_view(), name="node.create"),
    path("nodes/new/", views.newnode, name="node.new"),
    path(
        "nodes/<str:pk>/",
        views.NodeDetailView.as_view(),
        name="node.detail",
    ),
    path(
        "nodes/<str:pk>/update/",
        views.NodeUpdateView.as_view(),
        name="node.update",
    ),
    path(
        "nodes/<str:pk>/delete/",
        views.NodeDeleteView.as_view(),
        name="node.delete",
    ),
]
