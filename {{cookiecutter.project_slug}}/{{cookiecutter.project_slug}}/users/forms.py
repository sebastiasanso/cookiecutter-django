from django.contrib.auth import get_user_model, forms
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _
from django.urls import reverse_lazy
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Div, HTML
from allauth.account.forms import LoginForm

User = get_user_model()


class UserChangeForm(forms.UserChangeForm):
    class Meta(forms.UserChangeForm.Meta):
        model = User
        fields = ('email',)


class UserCreationForm(forms.UserCreationForm):

    error_message = forms.UserCreationForm.error_messages.update(
        {"duplicate_email": _("This email has already been taken.")}
    )

    class Meta(forms.UserCreationForm.Meta):
        model = User
        fields = ('email',)

    def clean_email(self):
        email = self.cleaned_data["email"]

        try:
            User.objects.get(email=email)
        except User.DoesNotExist:
            return email

        raise ValidationError(self.error_messages["duplicate_email"])

########################
# PublicLoginForm
########################
CUSTOM_LOGIN_SUBMIT = '{% raw %}<input type="submit" class="btn btn-primary" value="%s" />{% endraw %}' % "Sign in"
CUSTOM_LOGIN_LOST_PASSWORD = '{% raw %}<a href="#">Lost password?</a>{% endraw %}'
CUSTOM_LOGIN_NOT_REGISTERED = '{% raw %}<p>%s <a href={%% url "account_signup" %%}>%s</a></p>{% endraw %}' % (
    _('Not registered?'), _('Register now!'))

class PublicLoginForm(LoginForm):

    class Meta():
        model = User

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            'login',
            'password',
            Div('remember', HTML(CUSTOM_LOGIN_LOST_PASSWORD), css_class="inline-group"),
            HTML(CUSTOM_LOGIN_SUBMIT),
            HTML(CUSTOM_LOGIN_NOT_REGISTERED),
        )