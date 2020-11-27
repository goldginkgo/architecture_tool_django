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

from architecture_tool_django.common.tasks import delete_list, sync_list
from architecture_tool_django.nodes.models import Node

from . import forms
from .models import List


class ListdefListView(LoginRequiredMixin, ListView):
    model = List
    context_object_name = "listdef_list"
    template_name = "listdefs/list.html"


class ListdefCreateView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = List
    form_class = forms.ListdefCreateForm
    template_name = "listdefs/create.html"
    success_message = "List %(key)s created successfully!"

    def get_success_url(self):
        return reverse_lazy("lists:listdef.detail", kwargs={"pk": self.object.pk})

    def form_valid(self, form):
        response = super(ListdefCreateView, self).form_valid(form)
        if settings.SYNC_TO_GITLAB:
            access_token = self.request.user.get_gitlab_access_token()
            sync_list.delay(self.object.key, access_token)
        return response


class ListdefUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = List
    context_object_name = "listdef"
    form_class = forms.ListdefUpdateForm
    template_name = "listdefs/update.html"
    success_message = "List %(key)s updated successfully!"

    def get_success_url(self):
        return reverse_lazy("lists:listdef.detail", kwargs={"pk": self.object.pk})

    def form_valid(self, form):
        response = super(ListdefUpdateView, self).form_valid(form)
        if settings.SYNC_TO_GITLAB:
            access_token = self.request.user.get_gitlab_access_token()
            sync_list.delay(self.object.key, access_token)
        return response


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

        context["attrs"] = ["key", "type"] + attributes
        context["edgetypes"] = edgetypes

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

        context["node_names"] = {}
        for node in Node.objects.all():
            context["node_names"][node.key] = node.attributeSet["name"]

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
        res = super(ListdefDeleteView, self).delete(request, *args, **kwargs)
        if settings.SYNC_TO_GITLAB:
            access_token = self.request.user.get_gitlab_access_token()
            delete_list.delay(obj.key, access_token)
        return res
