from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.db.models import Q
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
from .models import Edgetype, Nodetype, Schema


class NodeTypeListView(LoginRequiredMixin, ListView):
    model = Nodetype
    context_object_name = "nodetype_list"
    template_name = "modeling/nodetypes/list.html"


class NodeTypeCreateView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = Nodetype
    form_class = forms.NodeTypeCreateForm
    template_name = "modeling/nodetypes/create.html"
    success_url = reverse_lazy("modeling:nodetype.list")
    success_message = "NodeType %(name)s created successfully!"


class NodeTypeUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = Nodetype
    context_object_name = "node_type"
    form_class = forms.NodeTypeUpdateForm
    template_name = "modeling/nodetypes/update.html"
    success_url = reverse_lazy("modeling:nodetype.list")
    success_message = "NodeType %(name)s updated successfully!"


class NodeTypeDetailView(LoginRequiredMixin, DetailView):
    model = Nodetype
    template_name = "modeling/nodetypes/detail.html"


class NodeTypeDeleteView(LoginRequiredMixin, SuccessMessageMixin, DeleteView):
    model = Nodetype
    success_url = reverse_lazy("modeling:nodetype.list")
    success_message = "NodeType %(name)s deleted successfully!"

    def delete(self, request, *args, **kwargs):
        obj = self.get_object()
        messages.success(self.request, self.success_message % obj.__dict__)
        return super(NodeTypeDeleteView, self).delete(request, *args, **kwargs)


@login_required(login_url="/accounts/login/")
def get_nodetypes_ajax(request):
    if request.GET.get("q"):
        nodetypes = Nodetype.objects.filter(name__iregex=request.GET.get("q"))
    else:
        nodetypes = Nodetype.objects.all()

    ret = {"results": []}
    for nodetype in nodetypes:
        ret["results"].append({"id": nodetype.key, "text": nodetype.name})

    return JsonResponse(ret)


class SchemaListView(LoginRequiredMixin, ListView):
    model = Schema
    context_object_name = "schema_list"
    template_name = "modeling/schemas/list.html"


class SchemaCreateView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = Schema
    form_class = forms.SchemaCreateForm
    template_name = "modeling/schemas/create.html"
    success_url = reverse_lazy("modeling:schema.list")
    success_message = "Schema %(key)s created successfully!"


class SchemaUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = Schema
    context_object_name = "schema"
    form_class = forms.SchemaUpdateForm
    template_name = "modeling/schemas/update.html"
    success_url = reverse_lazy("modeling:schema.list")
    success_message = "Schema %(key)s updated successfully!"


class SchemaDetailView(LoginRequiredMixin, DetailView):
    model = Schema
    template_name = "modeling/schemas/detail.html"


class SchemaDeleteView(LoginRequiredMixin, SuccessMessageMixin, DeleteView):
    model = Schema
    success_url = reverse_lazy("modeling:schema.list")
    success_message = "Schema %(key)s deleted successfully!"

    def delete(self, request, *args, **kwargs):
        obj = self.get_object()
        messages.success(self.request, self.success_message % obj.__dict__)
        return super(SchemaDeleteView, self).delete(request, *args, **kwargs)


class EdgeTypeListView(LoginRequiredMixin, ListView):
    model = Edgetype
    context_object_name = "edgetype_list"
    template_name = "modeling/edgetypes/list.html"


class EdgeTypeCreateView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = Edgetype
    form_class = forms.EdgeTypeCreateForm
    template_name = "modeling/edgetypes/create.html"
    success_url = reverse_lazy("modeling:edgetype.list")
    success_message = "EdgeType %(edgetype)s created successfully!"


class EdgeTypeUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = Edgetype
    context_object_name = "edgetype"
    form_class = forms.EdgeTypeUpdateForm
    template_name = "modeling/edgetypes/update.html"
    success_url = reverse_lazy("modeling:edgetype.list")
    success_message = "EdgeType %(edgetype)s updated successfully!"


class EdgeTypeDetailView(LoginRequiredMixin, DetailView):
    model = Edgetype
    template_name = "modeling/edgetypes/detail.html"


class EdgeTypeDeleteView(LoginRequiredMixin, SuccessMessageMixin, DeleteView):
    model = Edgetype
    success_url = reverse_lazy("modeling:edgetype.list")
    success_message = "EdgeType %(edgetype)s deleted successfully!"

    def delete(self, request, *args, **kwargs):
        obj = self.get_object()
        messages.success(self.request, self.success_message % obj.__dict__)
        return super(EdgeTypeDeleteView, self).delete(request, *args, **kwargs)


@login_required(login_url="/accounts/login/")
def get_edgetypes_ajax(request):
    src_nodetype = request.GET.get("src_nodetype")
    search = request.GET.get("search")

    if search:
        edgetypes = Edgetype.objects.filter(
            Q(source_nodetype__key=src_nodetype) & Q(edgetype_name__iregex=search)
        )
    else:
        edgetypes = Edgetype.objects.filter(source_nodetype__key=src_nodetype)

    ret = {"results": []}
    for edgetype in edgetypes:
        text = f"{edgetype.edgetype} -> [{edgetype.target_nodetype.key}]"
        ret["results"].append({"id": edgetype.id, "text": text})
    print(ret)
    return JsonResponse(ret)


@login_required(login_url="/accounts/login/")
def get_edgetype_ajax(request, pk):
    edgetype = Edgetype.objects.get(id=pk)
    text = f"{edgetype.edgetype} -> [{edgetype.target_nodetype.key}]"
    return JsonResponse({"id": edgetype.id, "text": text})
