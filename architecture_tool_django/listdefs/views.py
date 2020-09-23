from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView

from .models import List


class ListdefView(LoginRequiredMixin, ListView):
    model = List
    context_object_name = "listdef_list"
    template_name = "listdefs/list.html"
