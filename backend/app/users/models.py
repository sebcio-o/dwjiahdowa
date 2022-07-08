from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _


class CustomUser(AbstractUser):
    verbose_name = "user"

    email = models.EmailField(_("email address"), blank=True, unique=True)

    USERNAME_FIELD = "email"
    EMAIL_FIELD = "email"
    REQUIRED_FIELDS = ["username"]

    FIELDS_TO_UPDATE = ["first_name", "last_name"]

    def get_username(self):
        return self.username

    def __str__(self):
        return self.email
