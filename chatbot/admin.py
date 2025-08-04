# chatbot/admin.py

from django.contrib import admin
from .models import ChatMessage

@admin.register(ChatMessage)
class ChatMessageAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'role', 'short_message', 'timestamp')
    list_filter = ('role', 'timestamp')
    search_fields = ('message', 'user__username')

    def short_message(self, obj):
        return obj.message[:50] + ('...' if len(obj.message) > 50 else '')
    short_message.short_description = 'Message'
