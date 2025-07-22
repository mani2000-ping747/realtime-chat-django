from django.contrib.auth.models import AbstractUser
from django.db import models
from django.conf import settings


class Message(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    room_name = models.CharField(max_length=255)
    content = models.TextField(blank=True)
    file_heading = models.CharField(max_length=255, blank=True)
    file = models.FileField(upload_to="chat_uploads/", null=True, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    gif_url = models.URLField(null=True, blank=True)
    is_sticker = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.user.username}: {self.content or self.file_heading or 'File'}"


class Room(models.Model):
    name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.name
