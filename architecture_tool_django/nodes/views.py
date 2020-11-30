from django.conf import settings
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.db.models import Q
from django.http.response import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse_lazy
from django.views.generic import DeleteView, DetailView, ListView

from architecture_tool_django.common.tasks import delete_node, sync_node
from architecture_tool_django.modeling.models import Edgetype, Nodetype

from .api.serializers import NodeSerializer
from .forms import NodeEditForm
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
        folder = obj.nodetype.folder
        source_nodes = list(obj.source_nodes.all().values_list("key", flat=True))
        messages.success(self.request, self.success_message % obj.__dict__)
        res = super(NodeDeleteView, self).delete(request, *args, **kwargs)

        if settings.SYNC_TO_GITLAB:
            access_token = self.request.user.get_gitlab_access_token()
            delete_node.delay(obj.key, folder, source_nodes, access_token)
        return res


@login_required(login_url="/accounts/login/")
def newnode(request):
    if request.method == "GET":
        return render(request, "nodes/new.html")


@login_required(login_url="/accounts/login/")
def update_node(request, pk):
    if request.method == "GET":
        node = Node.objects.get(key=pk)
        nodetype_key = Nodetype.objects.get(name=node.nodetype).key
        outbound_edges = node.outbound_edges.all()
        return render(request, "nodes/update.html", locals())


@login_required(login_url="/accounts/login/")
def edit_node(request, pk):
    instance = get_object_or_404(Node, pk=pk)
    if request.method == "POST":
        form = NodeEditForm(request.POST)
        if form.is_valid():
            try:
                nodejson = form.cleaned_data["nodejson"]
                instance.remove_all_edges()
                for edge in nodejson["outbound_edges"]:
                    target_node = Node.objects.get(key=edge["target"])
                    edge_type = Edgetype.objects.get(
                        Q(source_nodetype=instance.nodetype)
                        & Q(target_nodetype=target_node.nodetype)
                        & Q(edgetype=edge["edge_type"])
                    )
                    instance.add_edge(target_node, edge_type)

                instance.attributeSet = nodejson.get(
                    "attributeSet", instance.attributeSet
                )
                instance.save()
                messages.success(request, f"Node {pk} updated successfully!")

                if settings.SYNC_TO_GITLAB:
                    access_token = request.user.get_gitlab_access_token()
                    sync_node.delay(pk, access_token)

                return HttpResponseRedirect(
                    reverse_lazy("nodes:node.detail", kwargs={"pk": pk})
                )

            except Exception as error:
                messages.error(request, error)
    else:
        serializer = NodeSerializer(instance)
        form = NodeEditForm(initial={"nodejson": serializer.data})

    context = {
        "form": form,
        "node_instance": instance,
    }

    return render(request, "nodes/edit.html", context)
