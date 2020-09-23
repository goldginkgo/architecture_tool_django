from django.urls import path

from architecture_tool_django.nodes import views

urlpatterns = [
    path("node_counts/", views.node_counts, name="node_counts"),
    path("nodes/", views.NodeView.as_view(), name="node.list"),
]
