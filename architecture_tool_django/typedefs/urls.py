from django.urls import path

from . import views

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
]
