from django.conf import settings
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from django.views.generic import (
    CreateView,
    DeleteView,
    DetailView,
    ListView,
    UpdateView,
)

from architecture_tool_django.common.tasks import delete_graph, sync_graph

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
    success_message = "Graph %(key)s created successfully!"

    def get_success_url(self):
        return reverse_lazy("graphs:graph.detail", kwargs={"pk": self.object.pk})

    def form_valid(self, form):
        response = super(GraphCreateView, self).form_valid(form)
        if settings.SYNC_TO_GITLAB:
            access_token = self.request.user.get_gitlab_access_token()
            sync_graph.delay(self.object.key, access_token)
        return response


class GraphUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = Graph
    context_object_name = "graph"
    form_class = forms.GraphUpdateForm
    template_name = "graphdefs/update.html"
    success_message = "Graph %(key)s updated successfully!"

    def get_success_url(self):
        return reverse_lazy("graphs:graph.detail", kwargs={"pk": self.object.pk})

    def form_valid(self, form):
        response = super(GraphUpdateView, self).form_valid(form)
        if settings.SYNC_TO_GITLAB:
            access_token = self.request.user.get_gitlab_access_token()
            sync_graph.delay(self.object.key, access_token)
        return response


class GraphDetailView(LoginRequiredMixin, DetailView):
    model = Graph
    template_name = "graphdefs/detail.html"

    def get_context_data(self, *args, **kwargs):
        context = super(GraphDetailView, self).get_context_data(*args, **kwargs)

        graph = self.get_object()

        graphkey = graph.key
        plantuml_server = settings.PLANTUML_SERVER_URL
        arctool_url = settings.ARCHITECTURE_TOOL_URL
        context["graphurl"] = (
            f"{plantuml_server}/proxy?cache=no&src="
            + f"{arctool_url}/api/graphs/{graphkey}/plantuml&fmt=svg"
        )

        return context


class GraphDeleteView(LoginRequiredMixin, SuccessMessageMixin, DeleteView):
    model = Graph
    success_url = reverse_lazy("graphs:graph.list")
    success_message = "Graph %(key)s deleted successfully!"

    def delete(self, request, *args, **kwargs):
        obj = self.get_object()
        messages.success(self.request, self.success_message % obj.__dict__)
        res = super(GraphDeleteView, self).delete(request, *args, **kwargs)
        if settings.SYNC_TO_GITLAB:
            access_token = self.request.user.get_gitlab_access_token()
            delete_graph.delay(obj.key, access_token)
        return res
