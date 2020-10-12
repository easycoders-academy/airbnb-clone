from django.contrib.auth.models import AbstractUser
from django.db import models

# Create your models here.
class User(AbstractUser):
    """ Кастомная модель пользователя """

    REQUIRED_FIELDS = ()

    GENDER_MALE = "мужчина"
    GENDER_FEMALE = "женщина"
    GENDER_OTHER = "другое"

    GENDER_CHOISES = (
        (GENDER_MALE, "Мужчина"),
        (GENDER_FEMALE, "Женщина"),
        (GENDER_OTHER, "Другое"),
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
        (CURRENCY_USD, "Доллар США"),
        (CURRENCY_RUB, "Российский рубль"),
    )

    avatar = models.ImageField(upload_to="avatars", blank=True)
    gender = models.CharField(max_length=10, choices=GENDER_CHOISES, blank=True)
    bio = models.TextField(default="", blank=True)
    birthdate = models.DateField(blank=True, null=True)
    language = models.CharField(
        choices=LANGUAGE_CHOISES, max_length=2, blank=True, default=LANGUAGE_RUSSIAN
    )
    currency = models.CharField(
        max_length=3, choices=CURRENCY_CHOISES, blank=True, default=CURRENCY_USD
    )
    superhost = models.BooleanField(default=False)
