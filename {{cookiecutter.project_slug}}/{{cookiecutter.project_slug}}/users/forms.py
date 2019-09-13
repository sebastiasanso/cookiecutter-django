from django.contrib.auth import get_user_model, forms
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _
from django.urls import reverse_lazy
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Div, HTML, ButtonHolder, Submit
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
CUSTOM_LOGIN_SUBMIT = '<input type="submit" class="btn btn-primary" value="%s" />' % "Sign in"
CUSTOM_LOGIN_LOST_PASSWORD = '<a href="#">Lost password?</a>'
CUSTOM_LOGIN_NOT_REGISTERED = '<p>%s <a href="%s">%s</a></p>' % (
    _('Not registered?'), reverse_lazy('account_signup'), _('Register now!'))


class PublicLoginForm(LoginForm):
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