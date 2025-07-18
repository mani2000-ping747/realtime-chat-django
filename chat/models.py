from django.contrib.auth.models import AbstractUser
from django.db import models


from django.conf import settings  # ✅ use settings.AUTH_USER_MODEL


from django.utils import timezone


class Message(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    room_name = models.CharField(max_length=255)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username}: {self.content}"
