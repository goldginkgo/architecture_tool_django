from django import template

register = template.Library()


@register.simple_tag
def avatar_url(user):
    if user.socialaccount_set.exists():
        return user.socialaccount_set.first().get_avatar_url()
    return "/static/images/avatar.png"


@register.simple_tag(takes_context=True)
def add_active(context, urlprefix, *args, **kwargs):
    return add_class(context, "active", urlprefix, *args, **kwargs)


@register.simple_tag(takes_context=True)
def add_menu_open(context, urlprefix, *args, **kwargs):
    return add_class(context, "menu-open", urlprefix, *args, **kwargs)


def add_class(context, classname, urlprefix, *args, **kwargs):
    exact_match = kwargs.pop("exact_match", False)
    not_when = kwargs.pop("not_when", "").split(",")
    not_when = [nw.strip() for nw in not_when if nw.strip()]

    current_path = context.request.path

    if not_when and any(nw in current_path for nw in not_when):
        return ""

    if not exact_match and current_path.startswith(urlprefix):
        return f" {classname} "
    elif exact_match and current_path == urlprefix:
        return f" {classname} "
    else:
        return ""


@register.simple_tag
def timeline_icon_style(action):
    if action == "add":
        return "fas fa-plus bg-blue"
    elif action == "update":
        return "fas fa-edit bg-green"
    elif action == "delete":
        return "fas fa-minus bg-red"
    elif action == "export":
        return "fas fa-download bg-blue"
    elif action == "import":
        return "fas fa-upload bg-green"
    else:
        return ""
