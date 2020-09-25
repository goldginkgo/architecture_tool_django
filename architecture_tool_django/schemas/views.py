from django.contrib.auth.decorators import login_required
from django.shortcuts import render

# from .models import Schema


@login_required(login_url="/accounts/login/")
def node(request):
    return render(request, "schemas/node.html")


@login_required(login_url="/accounts/login/")
def list(request):
    return render(request, "schemas/list.html")


@login_required(login_url="/accounts/login/")
def graph(request):
    return render(request, "schemas/graph.html")
