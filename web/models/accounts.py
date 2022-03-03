from django.conf import settings
from django.db import models
from django.core.validators import MinLengthValidator, EmailValidator

from .base import BaseModel


class ActivateToken(BaseModel):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE
    )
    activation_token = models.CharField(max_length=64, unique=True)


class Profile(BaseModel):
    id = models.AutoField(primary_key=True)
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE
    )
    phone_number = models.CharField(
        verbose_name="Numer telefonu", max_length=18
    )

    nip_number = models.CharField(
        verbose_name="Numer nip",
        validators=[MinLengthValidator(10)],
        max_length=13,
        null=True,
        blank=True,
    )
    company_name = models.CharField(
        verbose_name="Nazwa firmy",
        max_length=128,
        null=True,
        blank=True,
    )
    company_name_l = models.CharField(
        verbose_name="Nazwa firmy c.d.",
        max_length=128,
        null=True,
        blank=True,
    )
    company = models.BooleanField(
        verbose_name="Profil firmowy?", default=False
    )

    class Meta:
        ordering = ("-id",)
        verbose_name_plural = "Profil użytkownika"

    def __str__(self):
        return "{}, {}, {}".format(
            self.user.username, self.user.first_name, self.user.last_name
        )


class Address(BaseModel):
    id = models.AutoField(primary_key=True)
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        null=True,
        blank=True,
        verbose_name="Użytkownik",
        on_delete=models.CASCADE,
    )
    street = models.CharField(verbose_name="Ulica", max_length=128)
    house = models.CharField(verbose_name="Nr domu", max_length=8)
    door = models.CharField(
        verbose_name="Nr lokalu", null=True, blank=True, max_length=8
    )
    city = models.CharField(verbose_name="Miasto", max_length=64)
    post_code = models.CharField(
        verbose_name="Kod pocztowy", max_length=6
    )

    class Meta:
        ordering = (
            "user",
            "-id",
        )
        verbose_name_plural = "Adresy"

    def __str__(self):
        return "{}, {}, {}".format(self.user, self.street, self.house)
