import json

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import (
    CreateView,
    DeleteView,
    DetailView,
    ListView,
    UpdateView,
)

from architecture_tool_django.modeling.models import Edgetype, Nodetype

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


@login_required(login_url="/accounts/login/")
def newnode(request):
    if request.method == "POST":
        json_data = json.loads(request.body)
        nodetype = Nodetype.objects.get(key=json_data["type"])
        node = Node.objects.create(
            key=json_data["key"],
            nodetype=nodetype,
            attributeSet=json_data["attributeSet"],
        )
        for edge in json_data["edges"]:
            target_node = Node.objects.get(key=edge["target"])
            edge_type = Edgetype.objects.get(key=edge["edge_type"])
            node.add_edge(target_node, edge_type)
        result = {"result": "node created successfully."}
        messages.add_message(
            request, messages.SUCCESS, f"Node {json_data['key']} created successfully!"
        )
        return JsonResponse(result)
    else:
        return render(request, "nodes/new.html")


@login_required(login_url="/accounts/login/")
def get_nodes_ajax(request):
    if request.GET.get("q"):
        nodes = Node.objects.filter(key__iregex=request.GET.get("q"))
    else:
        nodes = Node.objects.all()

    ret = {"results": []}
    for node in nodes:
        ret["results"].append({"id": node.key, "text": str(node)})

    return JsonResponse(ret)


@login_required(login_url="/accounts/login/")
def get_node_ajax(request, pk):
    node = Node.objects.get(key=pk)
    return JsonResponse({"id": node.key, "text": str(node)})


@login_required(login_url="/accounts/login/")
def edit_node(request, pk):
    if request.method == "POST":
        json_data = json.loads(request.body)
        node = Node.objects.get(key=pk)

        node.attributeSet = json_data["attributeSet"]
        node.save()

        node.remove_all_edges()
        for edge in json_data["edges"]:
            target_node = Node.objects.get(key=edge["target"])
            edge_type = Edgetype.objects.get(key=edge["edge_type"])
            node.add_edge(target_node, edge_type)

        result = {"result": "node created successfully."}
        messages.add_message(
            request, messages.SUCCESS, f"Node {pk} updated successfully!"
        )
        return JsonResponse(result)
    else:
        node = Node.objects.get(key=pk)
        nodetype_key = Nodetype.objects.get(name=node.nodetype).key
        node_attributes = json.dumps(node.attributeSet)
        outbound_edges = node.outbound_edges.all()
        return render(request, "nodes/edit.html", locals())
