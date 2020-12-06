from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.shortcuts import render  # get_object_or_404, redirect

from architecture_tool_django.nodes.models import Node
from architecture_tool_django.utils.utils import recent_user_actions


@login_required(login_url="/accounts/login/")
def dashboard(request):
    User = get_user_model()
    users = User.objects.order_by("-date_joined")
    total_users = users.count()

    user_info = {}
    for user in users[:8]:
        user_info[user.username] = {}
        if user.get_full_name():
            user_info[user.username]["display_name"] = user.get_full_name()
        else:
            user_info[user.username]["display_name"] = user.username
        user_info[user.username]["date_joined"] = user.date_joined
        social_account = user.socialaccount_set.all().first()
        if social_account:
            user_info[user.username]["avatar_url"] = social_account.get_avatar_url()

    recent_nodes = Node.objects.order_by("-updated")[:5]

    return render(
        request,
        "pages/dashboard.html",
        {
            "user_info": user_info,
            "total_users": total_users,
            "recent_nodes": recent_nodes,
            "user_actions": recent_user_actions,
        },
    )


@login_required(login_url="/accounts/login/")
def contacts(request):
    return render(request, "pages/contacts.html")


@login_required(login_url="/accounts/login/")
def apis(request):
    return render(request, "pages/apis.html")


@login_required(login_url="/accounts/login/")
def faq(request):
    return render(request, "pages/faq.html")


@login_required(login_url="/accounts/login/")
def settings(request):
    return render(request, "pages/settings.html")
