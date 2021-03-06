from allauth.socialaccount.models import SocialToken
from django.contrib.auth.models import AbstractUser
from django.db.models import CharField
from django.urls import reverse
from django.utils.translation import gettext_lazy as _


class User(AbstractUser):
    """Default user for Architecture Tool."""

    #: First and last name do not cover name patterns around the globe
    name = CharField(_("Name of User"), blank=True, max_length=255)

    def get_absolute_url(self):
        """Get url for user's detail view.

        Returns:
            str: URL for user detail.

        """
        return reverse("users:detail", kwargs={"username": self.username})

    def get_gitlab_access_token(self):
        """Get GitLab access token for the user.

        Returns:
            str: GitLab access token.

        """
        token = SocialToken.objects.filter(
            account__user=self, account__provider="gitlab"
        ).first()
        return token.token if token else None
