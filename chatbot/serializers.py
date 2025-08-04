# serializers.py

from rest_framework import serializers
from .models import ChatMessage

class ChatMessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ChatMessage
        fields = ['id', 'user', 'role', 'message', 'timestamp']
        read_only_fields = ['user', 'timestamp']
