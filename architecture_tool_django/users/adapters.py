from typing import Any

from allauth.account.adapter import DefaultAccountAdapter
from allauth.socialaccount.adapter import DefaultSocialAccountAdapter
from django.conf import settings
from django.http import HttpRequest


class AccountAdapter(DefaultAccountAdapter):
    def is_open_for_signup(self, request: HttpRequest):
        return getattr(settings, "ACCOUNT_ALLOW_REGISTRATION", True)


class SocialAccountAdapter(DefaultSocialAccountAdapter):
    def is_open_for_signup(self, request: HttpRequest, sociallogin: Any):
        print("----------------------------------------------------1")
        print("----------------------------------------------------1")
        print("----------------------------------------------------1")
        print("----------------------------------------------------1")
        print("----------------------------------------------------1")
        return getattr(settings, "ACCOUNT_ALLOW_REGISTRATION", True)

    # For troubshooting authentication failures, to be removed in the future
    def authentication_error(
        self, request, provider_id, error=None, exception=None, extra_context=None
    ):
        print("----------------------------------------------------2")
        print("----------------------------------------------------2")
        print("----------------------------------------------------2")
        print("----------------------------------------------------2")
        print("----------------------------------------------------2")
        print("----------------------------------------------------2")
        print(provider_id)
        print(request)
        print(error)
        print(exception)
        print(extra_context)
