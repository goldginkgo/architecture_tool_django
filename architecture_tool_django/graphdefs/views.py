from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.http import JsonResponse
from django.urls import reverse_lazy
from django.views.generic import (
    CreateView,
    DeleteView,
    DetailView,
    ListView,
    UpdateView,
)

from . import forms
from .models import Graph


class GraphListView(LoginRequiredMixin, ListView):
    model = Graph
    context_object_name = "graph_list"
    template_name = "graphdefs/list.html"


class GraphCreateView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = Graph
    form_class = forms.GraphCreateForm
    template_name = "graphdefs/create.html"
    success_url = reverse_lazy("graphs:graph.list")
    success_message = "Graph %(key)s created successfully!"


class GraphUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = Graph
    context_object_name = "graph"
    form_class = forms.GraphUpdateForm
    template_name = "graphdefs/update.html"
    success_url = reverse_lazy("graphs:graph.list")
    success_message = "Graph %(key)s updated successfully!"


class GraphDetailView(LoginRequiredMixin, DetailView):
    model = Graph
    template_name = "graphs/detail.html"


class GraphDeleteView(LoginRequiredMixin, SuccessMessageMixin, DeleteView):
    model = Graph
    success_url = reverse_lazy("graphs:graph.list")
    success_message = "Graph %(key)s deleted successfully!"

    def delete(self, request, *args, **kwargs):
        obj = self.get_object()
        messages.success(self.request, self.success_message % obj.__dict__)
        return super(GraphDeleteView, self).delete(request, *args, **kwargs)


@login_required(login_url="/accounts/login/")
def get_graph(request, pk):
    graph = Graph.objects.get(key=pk).graph
    return JsonResponse(graph)
