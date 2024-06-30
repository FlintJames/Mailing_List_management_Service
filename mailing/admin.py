from django.contrib import admin
from mailing.models import Client, Mailing, Message, Attempt, Blog


@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = ['pk', 'full_name', 'email']
    search_fields = ['full_name', 'email']


@admin.register(Mailing)
class MailingAdmin(admin.ModelAdmin):
    list_display = ['pk', 'time_sending', 'periodicity', 'status']


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ['pk', 'subject']


@admin.register(Attempt)
class AttemptAdmin(admin.ModelAdmin):
    list_display = ['pk', 'status']

@admin.register(Blog)
class BlogAdmin(admin.ModelAdmin):
    list_display = ['pk', 'title', 'created_at']
