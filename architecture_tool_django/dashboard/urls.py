from django.urls import path

from architecture_tool_django.dashboard import views

urlpatterns = [
    path("contacts/", views.contacts, name="contacts"),
    path("apis/", views.apis, name="apis"),
    path("faq/", views.faq, name="faq"),
    # The home page
    path("", views.dashboard, name="home"),
]
