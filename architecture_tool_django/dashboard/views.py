from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.shortcuts import render  # get_object_or_404, redirect


@login_required(login_url="/accounts/login/")
def dashboard(request):
    User = get_user_model()
    users = User.objects.order_by("-date_joined")
    total_users = users.count()

    user_info = {}
    for user in users[:9]:
        user_info[user.username] = {}
        user_info[user.username]["date_joined"] = user.date_joined
        social_account = user.socialaccount_set.all().first()
        if social_account:
            user_info[user.username]["avatar_url"] = social_account.get_avatar_url()

    return render(
        request, "pages/home.html", {"user_info": user_info, "total_users": total_users}
    )


@login_required(login_url="/accounts/login/")
def contacts(request):
    return render(request, "pages/contacts.html")
