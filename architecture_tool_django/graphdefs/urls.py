from django.urls import path

from . import views

urlpatterns = [
    path("graphs/", views.GraphListView.as_view(), name="graph.list"),
]
