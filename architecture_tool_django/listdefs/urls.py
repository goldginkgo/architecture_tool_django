from django.urls import path

from . import views

urlpatterns = [
    path("lists/", views.ListdefView.as_view(), name="listdef.list"),
]
