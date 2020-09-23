from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse
from django.views.generic import ListView

from .models import Node

# from django.shortcuts import render


@login_required(login_url="/accounts/login/")
def node_counts(request):
    count = Node.objects.all().count()
    return HttpResponse(count)


class NodeView(LoginRequiredMixin, ListView):
    model = Node
    context_object_name = "node_list"
    template_name = "nodes/list.html"
