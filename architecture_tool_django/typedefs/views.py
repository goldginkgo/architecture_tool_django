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

from . import forms
from .models import Edgetype, Nodetype


class NodeTypeListView(LoginRequiredMixin, ListView):
    model = Nodetype
    context_object_name = "nodetype_list"
    template_name = "typedefs/nodetypes/list.html"


class NodeTypeCreateView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = Nodetype
    form_class = forms.NodeTypeCreateForm
    template_name = "typedefs/nodetypes/create.html"
    success_url = reverse_lazy("nodetype.list")
    success_message = "NodeType %(name)s created successfully!"


class NodeTypeUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = Nodetype
    context_object_name = "node_type"
    form_class = forms.NodeTypeUpdateForm
    template_name = "typedefs/nodetypes/update.html"
    success_url = reverse_lazy("nodetype.list")
    success_message = "NodeType %(name)s updated successfully!"


class NodeTypeDetailView(LoginRequiredMixin, DetailView):
    model = Nodetype
    template_name = "typedefs/nodetypes/detail.html"


class NodeTypeDeleteView(LoginRequiredMixin, SuccessMessageMixin, DeleteView):
    model = Nodetype
    success_url = reverse_lazy("nodetype.list")
    success_message = "NodeType %(name)s deleted successfully!"

    def delete(self, request, *args, **kwargs):
        obj = self.get_object()
        messages.success(self.request, self.success_message % obj.__dict__)
        return super(NodeTypeDeleteView, self).delete(request, *args, **kwargs)


class EdgeTypeListView(LoginRequiredMixin, ListView):
    model = Edgetype
    context_object_name = "edgetype_list"
    template_name = "typedefs/edgetypes/list.html"
