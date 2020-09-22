from django import template

register = template.Library()


@register.simple_tag
def avatar_url(user):
    if user.socialaccount_set.exists():
        return user.socialaccount_set.first().get_avatar_url()
    return "/static/images/avatar.png"
