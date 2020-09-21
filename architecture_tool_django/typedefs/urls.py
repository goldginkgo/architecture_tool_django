from django.urls import path

from . import views

urlpatterns = [
    path("nodetypes/", views.NodeTypeListView.as_view(), name="nodetype.list"),
    path(
        "nodetypes/create/", views.NodeTypeCreateView.as_view(), name="nodetype.create"
    ),
    path(
        "nodetypes/<int:pk>/",
        views.NodeTypeUpdateView.as_view(),
        name="nodetype.detail",
    ),
    path(
        "nodetypes/<int:pk>/update/",
        views.NodeTypeDetailView.as_view(),
        name="nodetype.update",
    ),
    path(
        "nodetypes/<int:pk>/delete/",
        views.NodeTypeDeleteView.as_view(),
        name="nodetype.delete",
    ),
]
