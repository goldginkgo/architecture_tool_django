from django.urls import path

from architecture_tool_django.common import views

urlpatterns = [
    path("export/", views.export, name="export"),
    path("download/<file_basename>/", views.download, name="download"),
    path("tasks/<task_id>/", views.get_status, name="get_status"),
]
