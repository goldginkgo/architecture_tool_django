from django import template
from django.urls import reverse

register = template.Library()


@register.simple_tag
def avatar_url(user):
    if user.socialaccount_set.exists():
        return user.socialaccount_set.first().get_avatar_url()
    return "/static/images/avatar.png"


@register.simple_tag(takes_context=True)
def add_active(context, url_name, *args, **kwargs):
    exact_match = kwargs.pop("exact_match", False)
    not_when = kwargs.pop("not_when", "").split(",")
    not_when = [nw.strip() for nw in not_when if nw.strip()]

    path = reverse(url_name, args=args, kwargs=kwargs)
    current_path = context.request.path

    if not_when and any(nw in current_path for nw in not_when):
        return ""

    if not exact_match and current_path.startswith(path):
        return " active "
    elif exact_match and current_path == path:
        return " active "
    else:
        return ""


@register.simple_tag(takes_context=True)
def add_menu_open(context, url_name, *args, **kwargs):
    exact_match = kwargs.pop("exact_match", False)
    not_when = kwargs.pop("not_when", "").split(",")
    not_when = [nw.strip() for nw in not_when if nw.strip()]

    path = reverse(url_name, args=args, kwargs=kwargs)
    current_path = context.request.path

    if not_when and any(nw in current_path for nw in not_when):
        return ""

    if not exact_match and current_path.startswith(path):
        return " menu-open "
    elif exact_match and current_path == path:
        return " menu-open "
    else:
        return ""
