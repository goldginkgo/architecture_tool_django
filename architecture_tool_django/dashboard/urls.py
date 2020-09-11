from django.urls import path, re_path

from architecture_tool_django.dashboard import views

urlpatterns = [
    # The home page
    path("", views.dashboard, name="dashboard"),
    # Matches any html file
    re_path(r"^.*\.*", views.pages, name="pages"),
]
