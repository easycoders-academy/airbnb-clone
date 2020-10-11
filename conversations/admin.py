from django.contrib import admin
from . import models


@admin.register(models.Conversation)
class ConversationAdmin(admin.ModelAdmin):
    """ Описание админки диалогов """

    list_display = ("__str__", "count_messages", "count_participants")


@admin.register(models.Message)
class MessageAdmin(admin.ModelAdmin):
    """ Описание админки сообщений """

    list_display = ("__str__", "created")
