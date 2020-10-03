from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.http import HttpResponse, JsonResponse
from django.urls import reverse_lazy
from django.views.generic import (
    CreateView,
    DeleteView,
    DetailView,
    ListView,
    UpdateView,
)

from . import forms
from .models import Node


@login_required(login_url="/accounts/login/")
def node_counts(request):
    count = Node.objects.all().count()
    return HttpResponse(count)


class NodeListView(LoginRequiredMixin, ListView):
    model = Node
    context_object_name = "node_list"
    template_name = "nodes/list.html"


class NodeCreateView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = Node
    form_class = forms.NodeCreateForm
    template_name = "nodes/create.html"
    success_url = reverse_lazy("nodes:node.list")
    success_message = "Node %(key)s created successfully!"


class NodeUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = Node
    context_object_name = "node"
    form_class = forms.NodeUpdateForm
    template_name = "nodes/update.html"
    success_url = reverse_lazy("nodes:node.list")
    success_message = "Node %(key)s updated successfully!"


class NodeDetailView(LoginRequiredMixin, DetailView):
    model = Node
    template_name = "nodes/detail.html"


class NodeDeleteView(LoginRequiredMixin, SuccessMessageMixin, DeleteView):
    model = Node
    success_url = reverse_lazy("nodes:node.list")
    success_message = "Node %(key)s deleted successfully!"

    def delete(self, request, *args, **kwargs):
        obj = self.get_object()
        messages.success(self.request, self.success_message % obj.__dict__)
        return super(NodeDeleteView, self).delete(request, *args, **kwargs)


@login_required(login_url="/accounts/login/")
def get_node(request, pk):
    attributeSet = Node.objects.get(key=pk).attributeSet
    return JsonResponse(attributeSet)
