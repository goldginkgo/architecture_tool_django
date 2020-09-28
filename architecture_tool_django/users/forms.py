from allauth.account.forms import LoginForm
from crispy_forms.bootstrap import AppendedText
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Div, Field, Layout, Row, Submit
from django.contrib.auth import forms, get_user_model
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

User = get_user_model()


class UserChangeForm(forms.UserChangeForm):
    class Meta(forms.UserChangeForm.Meta):
        model = User


class UserCreationForm(forms.UserCreationForm):

    error_message = forms.UserCreationForm.error_messages.update(
        {"duplicate_username": _("This username has already been taken.")}
    )

    class Meta(forms.UserCreationForm.Meta):
        model = User

    def clean_username(self):
        username = self.cleaned_data["username"]

        try:
            User.objects.get(username=username)
        except User.DoesNotExist:
            return username

        raise ValidationError(self.error_messages["duplicate_username"])


class CustomCheckbox(Field):
    template = "custom_crispy_fields/custom_checkbox.html"


class MyLoginForm(LoginForm):
    # override singup form from django-allauth
    def __init__(self, *args, **kwargs):
        super(MyLoginForm, self).__init__(*args, **kwargs)

        self.helper = FormHelper(self)
        self.fields["login"].label = False
        self.fields["password"].label = False

        self.helper.layout = Layout(
            AppendedText("login", '<span class="fas fa-envelope"></span>'),
            AppendedText("password", '<span class="fas fa-lock"></span>'),
            Row(
                Div(
                    Div(
                        CustomCheckbox("remember"),
                    ),
                    css_class="col-8",
                ),
                Div(
                    Submit("submit", "Sign In", css_class="btn-block"),
                    css_class="col-4",
                ),
            ),
        )
