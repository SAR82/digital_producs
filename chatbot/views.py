# views.py

from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .models import ChatMessage
from .serializers import ChatMessageSerializer
import requests
import json
import re


OLLAMA_URL = "http://localhost:11434/api/chat"


def clean_bot_response(text):
    text = text.replace('\n', ' ').replace('  ', ' ')

    text = re.sub(r'\*\*(.*?)\*\*', r'\1', text)

    return text.strip()


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def chat_with_bot(request):
    user = request.user
    user_message = request.data.get('message')

    if not user_message:
        return Response({'error': 'پیام خالی است'}, status=400)

    ChatMessage.objects.create(user=user, role='user', message=user_message)

    history = ChatMessage.objects.filter(user=user).order_by('timestamp')
    formatted_messages = [
        {'role': msg.role, 'content': msg.message}
        for msg in history
    ]

    payload = {
        "model": "gemma3:1b", 
        "messages": formatted_messages
    }


    try:

        ollama_response = requests.post(OLLAMA_URL, json=payload)
        lines = ollama_response.text.strip().splitlines()
        full_reply = ""

        for line in lines:
            try:
                chunk = json.loads(line)
                content = chunk.get("message", {}).get("content", "")
                full_reply += content
            except json.JSONDecodeError as e:
                print("خطا در پردازش یک خط JSON:", e)
                continue

        if not full_reply:
            return Response({'error': 'پاسخ معتبری از ربات دریافت نشد'}, status=500)

        bot_reply = full_reply
        bot_reply = clean_bot_response(full_reply)


        ChatMessage.objects.create(user=user, role='bot', message=bot_reply)

    except Exception as e:
        return Response({'error': str(e)}, status=500)

    return Response({'response': bot_reply})
