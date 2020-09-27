from django.urls import path

from . import views

app_name = "lists"
urlpatterns = [
    path("listcount/", views.listdef_count, name="listdef.count"),
    path("lists/", views.ListdefListView.as_view(), name="listdef.list"),
    path("lists/create/", views.ListdefCreateView.as_view(), name="listdef.create"),
    path(
        "lists/<str:pk>/",
        views.ListdefDetailView.as_view(),
        name="listdef.detail",
    ),
    path(
        "lists/<str:pk>/update/",
        views.ListdefUpdateView.as_view(),
        name="listdef.update",
    ),
    path(
        "lists/<str:pk>/delete/",
        views.ListdefDeleteView.as_view(),
        name="listdef.delete",
    ),
    path("listapi/<str:pk>/", views.get_listdef, name="listdefapi"),
]
