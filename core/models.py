from django.db import models
from . import managers

# Create your models here.
class TimeStampedModel(models.Model):
    """ Общие поля с ДатойВременем """

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    objects = managers.CustomModelManager()

    class Meta:
        abstract = True