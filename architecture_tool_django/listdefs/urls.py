from django.urls import path

from . import views

urlpatterns = [
    path("listcount/", views.listdef_count, name="listdef.count"),
    path("lists/", views.ListdefView.as_view(), name="listdef.list"),
]
