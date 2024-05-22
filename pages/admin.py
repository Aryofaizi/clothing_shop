from django.contrib import admin
from .models import Message

@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    model = Message
    list_display = ("name", "email", "subject", "text", "datetime_created")

    

