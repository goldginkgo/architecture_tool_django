from django.urls import path

from architecture_tool_django.dashboard import views

urlpatterns = [
    # The Contacts page
    path("contacts/", views.contacts, name="contacts"),
    # The home page
    path("", views.dashboard, name="home"),
]
