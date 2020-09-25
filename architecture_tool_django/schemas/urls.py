from django.urls import path

from architecture_tool_django.schemas import views

urlpatterns = [
    path("schemas/node/", views.node, name="schema.node"),
    path("schemas/list/", views.list, name="schema.list"),
    path("schemas/graph/", views.graph, name="schema.graph"),
]
