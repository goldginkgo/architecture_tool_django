from django.conf import settings
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import DeleteView, DetailView, ListView

from architecture_tool_django.modeling.models import Nodetype

from .models import Node


class NodeListView(LoginRequiredMixin, ListView):
    model = Node
    context_object_name = "node_list"
    template_name = "nodes/list.html"


class NodeDetailView(LoginRequiredMixin, DetailView):
    model = Node
    template_name = "nodes/detail.html"

    def get_context_data(self, *args, **kwargs):
        context = super(NodeDetailView, self).get_context_data(*args, **kwargs)

        node = self.get_object()

        nodekey = node.key
        plantuml_server = settings.PLANTUML_SERVER_URL
        arctool_url = settings.ARCHITECTURE_TOOL_URL
        context["graphurl"] = (
            f"{plantuml_server}/proxy?cache=no&src="
            + f"{arctool_url}/api/nodes/{nodekey}/plantuml&fmt=svg"
        )

        context["outbound_edges"] = node.outbound_edges.all()
        context["inbound_edges"] = node.inbound_edges.all()

        return context


class NodeDeleteView(LoginRequiredMixin, SuccessMessageMixin, DeleteView):
    model = Node
    success_url = reverse_lazy("nodes:node.list")
    success_message = "Node %(key)s deleted successfully!"

    def delete(self, request, *args, **kwargs):
        obj = self.get_object()
        messages.success(self.request, self.success_message % obj.__dict__)
        return super(NodeDeleteView, self).delete(request, *args, **kwargs)


@login_required(login_url="/accounts/login/")
def newnode(request):
    if request.method == "GET":
        return render(request, "nodes/new.html")


@login_required(login_url="/accounts/login/")
def edit_node(request, pk):
    if request.method == "GET":
        node = Node.objects.get(key=pk)
        nodetype_key = Nodetype.objects.get(name=node.nodetype).key
        outbound_edges = node.outbound_edges.all()
        return render(request, "nodes/edit.html", locals())
