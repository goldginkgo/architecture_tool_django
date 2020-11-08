from django.urls import path

from . import views

app_name = "graphs"
urlpatterns = [
    path("graphs/", views.GraphListView.as_view(), name="graph.list"),
    path("graphs/create/", views.GraphCreateView.as_view(), name="graph.create"),
    path(
        "graphs/<str:pk>/",
        views.GraphDetailView.as_view(),
        name="graph.detail",
    ),
    path(
        "graphs/<str:pk>/update/",
        views.GraphUpdateView.as_view(),
        name="graph.update",
    ),
    path(
        "graphs/<str:pk>/delete/",
        views.GraphDeleteView.as_view(),
        name="graph.delete",
    ),
]
