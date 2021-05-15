import uuid
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.core.mail import send_mail
from django.conf import settings
from django.utils.html import strip_tags
from django.shortcuts import reverse
from django.template.loader import render_to_string
from django.utils.translation import gettext_lazy as _

# Create your models here.
class User(AbstractUser):
    """ Кастомная модель пользователя """

    REQUIRED_FIELDS = ()

    GENDER_MALE = "мужчина"
    GENDER_FEMALE = "женщина"
    GENDER_OTHER = "другое"

    GENDER_CHOISES = (
        (GENDER_MALE, _("Мужчина")),
        (GENDER_FEMALE, _("Женщина")),
        (GENDER_OTHER, _("Другое")),
    )

    LANGUAGE_ENGLISH = "en"
    LANGUAGE_RUSSIAN = "ru"

    LANGUAGE_CHOISES = (
        (LANGUAGE_ENGLISH, "English"),
        (LANGUAGE_RUSSIAN, "Русский"),
    )

    CURRENCY_USD = "usd"
    CURRENCY_RUB = "rub"

    CURRENCY_CHOISES = (
        (CURRENCY_USD, _("Доллар США")),
        (CURRENCY_RUB, _("Российский рубль")),
    )

    LOGIN_EMAIL = "email"
    LOGIN_GITHUB = "github"
    LOGIN_VK = "vk"

    LOGIN_CHOICES = ((LOGIN_EMAIL, "Email"), (LOGIN_GITHUB, "Github"), (LOGIN_VK, "VK"))

    avatar = models.ImageField(upload_to="avatars", blank=True)
    gender = models.CharField(
        _("Пол"), max_length=10, choices=GENDER_CHOISES, blank=True
    )
    bio = models.TextField(_("О себе"), default="", blank=True)
    birthdate = models.DateField(blank=True, null=True)
    language = models.CharField(
        choices=LANGUAGE_CHOISES, max_length=2, blank=True, default=LANGUAGE_RUSSIAN
    )
    currency = models.CharField(
        max_length=3, choices=CURRENCY_CHOISES, blank=True, default=CURRENCY_USD
    )
    superhost = models.BooleanField(_("Суперхост"), default=False)
    email_verified = models.BooleanField(default=False)
    email_secret = models.CharField(max_length=20, default="", blank=True)
    login_method = models.CharField(
        max_length=50, choices=LOGIN_CHOICES, default=LOGIN_EMAIL
    )

    def get_absolute_url(self):
        return reverse("users:profile", kwargs={"pk": self.pk})

    def verify_email(self):
        if self.email_verified is False:
            secret = uuid.uuid4().hex[:20]
            self.email_secret = secret
            html_message = render_to_string(
                "emails/verify_email.html", context={"secret": secret}
            )
            send_mail(
                "Подтверждение аккаунта AirBnb",
                strip_tags(html_message),
                settings.EMAIL_FROM,
                [self.email],
                fail_silently=False,
                html_message=html_message,
            )
            self.save()
        return
