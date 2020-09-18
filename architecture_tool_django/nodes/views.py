from django.contrib.auth.decorators import login_required
from django.http import HttpResponse

from .models import Node

# from django.shortcuts import render


@login_required(login_url="/accounts/login/")
def node_counts(request):
    count = Node.objects.all().count()
    return HttpResponse(count)
