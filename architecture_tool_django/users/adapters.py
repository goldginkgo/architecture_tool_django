import logging
from typing import Any

from allauth.account.adapter import DefaultAccountAdapter
from allauth.socialaccount.adapter import DefaultSocialAccountAdapter
from django.conf import settings
from django.http import HttpRequest

logger = logging.getLogger(__name__)


class AccountAdapter(DefaultAccountAdapter):
    def is_open_for_signup(self, request: HttpRequest):
        return getattr(settings, "ACCOUNT_ALLOW_REGISTRATION", True)


class SocialAccountAdapter(DefaultSocialAccountAdapter):
    def is_open_for_signup(self, request: HttpRequest, sociallogin: Any):
        logger.info("----------------------------------------------------")
        return getattr(settings, "ACCOUNT_ALLOW_REGISTRATION", True)

    # For troubshooting authentication failures, to be removed in the future
    def authentication_error(
        self, request, provider_id, error=None, exception=None, extra_context=None
    ):
        logger.error("----------------------------------------------------")
        logger.error(provider_id)
        logger.error(request)
        logger.error(error)
        logger.error(exception)
        logger.error(extra_context)
