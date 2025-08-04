
from django.db import models
from django.conf import settings

class ChatMessage(models.Model):
    ROLE_CHOICES = (
        ('user', 'User'),
        ('bot', 'Bot'),
    )

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    role = models.CharField(max_length=10, choices=ROLE_CHOICES)
    message = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.role}: {self.message[:30]}"
