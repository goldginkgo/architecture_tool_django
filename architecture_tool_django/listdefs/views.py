from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse
from django.views.generic import ListView

from .models import List


@login_required(login_url="/accounts/login/")
def listdef_count(request):
    count = List.objects.all().count()
    return HttpResponse(count)


class ListdefView(LoginRequiredMixin, ListView):
    model = List
    context_object_name = "listdef_list"
    template_name = "listdefs/list.html"
