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

from architecture_tool_django.common.tasks import (
    delete_edgetype,
    delete_nodetype,
    delete_schema,
    sync_edgetypes,
    sync_nodetypes,
    sync_schema,
)
from architecture_tool_django.utils.utils import log_user_action

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

    def form_valid(self, form):
        response = super(NodeTypeCreateView, self).form_valid(form)

        rc = self.request.POST["key"]
        log_user_action(self.request.user, "add", "nodetype", rc)

        if settings.SYNC_TO_GITLAB:
            access_token = self.request.user.get_gitlab_access_token()
            sync_nodetypes.delay(access_token)
        return response


class NodeTypeUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = Nodetype
    context_object_name = "node_type"
    form_class = forms.NodeTypeUpdateForm
    template_name = "modeling/nodetypes/update.html"
    success_url = reverse_lazy("modeling:nodetype.list")
    success_message = "NodeType %(name)s updated successfully!"

    def form_valid(self, form):
        response = super(NodeTypeUpdateView, self).form_valid(form)

        rc = self.request.POST["key"]
        log_user_action(self.request.user, "update", "nodetype", rc)

        if settings.SYNC_TO_GITLAB:
            access_token = self.request.user.get_gitlab_access_token()
            sync_nodetypes.delay(access_token)
        return response


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
        ret = super(NodeTypeDeleteView, self).delete(request, *args, **kwargs)

        log_user_action(self.request.user, "delete", "nodetype", obj.key)

        if settings.SYNC_TO_GITLAB:
            access_token = self.request.user.get_gitlab_access_token()
            delete_nodetype.delay(access_token)
        return ret


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

    def form_valid(self, form):
        response = super(SchemaCreateView, self).form_valid(form)

        rc = self.request.POST["key"]
        log_user_action(self.request.user, "add", "schema", rc)

        if settings.SYNC_TO_GITLAB:
            access_token = self.request.user.get_gitlab_access_token()
            sync_schema.delay(self.object.key, access_token)
        return response


class SchemaUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = Schema
    context_object_name = "schema"
    form_class = forms.SchemaUpdateForm
    template_name = "modeling/schemas/update.html"
    success_url = reverse_lazy("modeling:schema.list")
    success_message = "Schema %(key)s updated successfully!"

    def form_valid(self, form):
        response = super(SchemaUpdateView, self).form_valid(form)

        rc = self.request.POST["key"]
        log_user_action(self.request.user, "update", "schema", rc)

        if settings.SYNC_TO_GITLAB:
            access_token = self.request.user.get_gitlab_access_token()
            sync_schema.delay(self.object.key, access_token)
        return response


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
        ret = super(SchemaDeleteView, self).delete(request, *args, **kwargs)

        log_user_action(self.request.user, "delete", "schema", obj.key)

        if settings.SYNC_TO_GITLAB:
            access_token = self.request.user.get_gitlab_access_token()
            delete_schema.delay(obj.key, access_token)
        return ret


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

    def form_valid(self, form):
        response = super(EdgeTypeCreateView, self).form_valid(form)

        log_user_action(self.request.user, "add", "edgetype", "")

        if settings.SYNC_TO_GITLAB:
            access_token = self.request.user.get_gitlab_access_token()
            sync_edgetypes.delay(access_token)
        return response


class EdgeTypeUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = Edgetype
    context_object_name = "edgetype"
    form_class = forms.EdgeTypeUpdateForm
    template_name = "modeling/edgetypes/update.html"
    success_url = reverse_lazy("modeling:edgetype.list")
    success_message = "EdgeType %(edgetype)s updated successfully!"

    def form_valid(self, form):
        response = super(EdgeTypeUpdateView, self).form_valid(form)

        log_user_action(self.request.user, "update", "edgetype", "")

        if settings.SYNC_TO_GITLAB:
            access_token = self.request.user.get_gitlab_access_token()
            sync_edgetypes.delay(access_token)
        return response


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
        ret = super(EdgeTypeDeleteView, self).delete(request, *args, **kwargs)

        log_user_action(self.request.user, "delete", "edgetype", "")

        if settings.SYNC_TO_GITLAB:
            access_token = self.request.user.get_gitlab_access_token()
            delete_edgetype.delay(access_token)

        return ret
