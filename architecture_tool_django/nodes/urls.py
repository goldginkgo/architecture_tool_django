from django.urls import path

from architecture_tool_django.nodes import views

app_name = "nodes"
urlpatterns = [
    path("nodes/", views.NodeListView.as_view(), name="node.list"),
    path("nodes/new/", views.newnode, name="node.new"),
    path(
        "nodes/<str:pk>/",
        views.NodeDetailView.as_view(),
        name="node.detail",
    ),
    path(
        "nodes/<str:pk>/update/",
        views.update_node,
        name="node.update",
    ),
    path(
        "nodes/<str:pk>/edit/",
        views.edit_node,
        name="node.edit",
    ),
    path(
        "nodes/<str:pk>/delete/",
        views.NodeDeleteView.as_view(),
        name="node.delete",
    ),
]
