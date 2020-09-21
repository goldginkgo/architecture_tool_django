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
from .models import Nodetype


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
    template_name = "typedefs/nodetypes/delete_confirm.html"
    success_url = reverse_lazy("typedefs:nodetype.list")
    success_message = "NodeType %(name)s deleted successfully!"
