from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView

from .models import Graph


class GraphListView(LoginRequiredMixin, ListView):
    model = Graph
    context_object_name = "graph_list"
    template_name = "graphdefs/list.html"
