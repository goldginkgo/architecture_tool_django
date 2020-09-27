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
