from django.contrib.auth.models import AbstractUser
from django.db import models
from phonenumber_field.modelfields import PhoneNumberField
from django.utils.translation import gettext_lazy as _

# Create your models here.


class User(AbstractUser):
    first_name = models.CharField(_("first name"), max_length=150,)
    last_name = models.CharField(_("last name"), max_length=150)
    email = models.EmailField(_("email address"))
    phone_number = PhoneNumberField(unique=True)

    class Meta:
        unique_together = ("email", "phone_number")
        verbose_name = "User"
        verbose_name_plural = "Users"
