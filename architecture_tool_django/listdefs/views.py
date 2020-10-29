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

from architecture_tool_django.nodes.models import Node

from . import forms
from .models import List


@login_required(login_url="/accounts/login/")
def listdef_count(request):
    count = List.objects.all().count()
    return HttpResponse(count)


class ListdefListView(LoginRequiredMixin, ListView):
    model = List
    context_object_name = "listdef_list"
    template_name = "listdefs/list.html"


class ListdefCreateView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = List
    form_class = forms.ListdefCreateForm
    template_name = "listdefs/create.html"
    success_url = reverse_lazy("lists:listdef.list")
    success_message = "List %(key)s created successfully!"


class ListdefUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = List
    context_object_name = "listdef"
    form_class = forms.ListdefUpdateForm
    template_name = "listdefs/update.html"
    success_url = reverse_lazy("lists:listdef.list")
    success_message = "List %(key)s updated successfully!"


class ListdefDetailView(LoginRequiredMixin, DetailView):
    model = List
    template_name = "listdefs/detail.html"

    def get_context_data(self, *args, **kwargs):
        context = super(ListdefDetailView, self).get_context_data(*args, **kwargs)

        context["listkey"] = self.get_object().key

        listdef = self.get_object().listdef
        nodetypes = listdef["nodes"]["filter"]["types"]
        nodetypes_regex = "|".join(nodetypes)

        attributes = listdef["nodes"]["attributes"]
        edgetypes = listdef["nodes"]["edges"]
        edge_direction = listdef["nodes"].get("edgeDirection")

        table_attrs = ["key", "type"] + attributes + edgetypes
        context["table_attrs"] = []
        [
            context["table_attrs"].append(x)
            for x in table_attrs
            if x not in context["table_attrs"]
        ]

        context["nodes"] = []
        nodes = Node.objects.filter(nodetype__key__iregex=nodetypes_regex)
        for node in nodes:
            item = {"key": node.key, "type": node.nodetype.key}

            for attribute in attributes:
                if attribute in node.attributeSet:
                    item[attribute] = node.attributeSet[attribute]

            for edgetype in edgetypes:
                item[edgetype] = []
                if self.outgoing_direction(edge_direction):
                    edges = list(
                        node.outbound_edges.filter(
                            edge_type__edgetype__iregex=edgetype
                        ).values_list("target__key", flat=True)
                    )
                    item[edgetype].extend(edges)
                if self.incoming_direction(edge_direction):
                    edges = list(
                        node.inbound_edges.filter(
                            edge_type__edgetype__iregex=edgetype
                        ).values_list("source__key", flat=True)
                    )
                    item[edgetype].extend(edges)

            context["nodes"].append(item)

        return context

    def outgoing_direction(self, direction):
        if direction is None:
            return True
        if direction == "out" or direction == "both":
            return True
        return False

    def incoming_direction(self, direction):
        if direction is None:
            return True
        if direction == "in" or direction == "both":
            return True
        return False


class ListdefDeleteView(LoginRequiredMixin, SuccessMessageMixin, DeleteView):
    model = List
    success_url = reverse_lazy("lists:listdef.list")
    success_message = "List %(key)s deleted successfully!"

    def delete(self, request, *args, **kwargs):
        obj = self.get_object()
        messages.success(self.request, self.success_message % obj.__dict__)
        return super(ListdefDeleteView, self).delete(request, *args, **kwargs)


@login_required(login_url="/accounts/login/")
def get_listdef(request, pk):
    listdef = List.objects.get(key=pk).listdef
    return JsonResponse(listdef)
