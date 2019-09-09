from django.contrib.auth.models import AbstractUser
from django.db.models import CharField
from django.urls import reverse
from django.utils.translation import ugettext_lazy as _
from .managers import UserManager


class User(AbstractUser):
    username = None
    email = EmailField(_('email'), unique=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = UserManager()

    def get_absolute_url(self):
        return reverse("users:detail", kwargs={"email": self.email})