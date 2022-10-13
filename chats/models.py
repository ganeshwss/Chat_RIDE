from platform import platform
from django.db import models
from django.contrib.auth.models import User
from django.dispatch import receiver

# Create your models here.


class ChatModel(models.Model):
    sender = models.CharField(max_length=50, default=None)
    receiver = models.CharField(max_length=50, default=None)
    message = models.TextField(null=True, blank=True)
    message_type = models.CharField(max_length=50, default=None)
    room_name = models.CharField(null=True, blank=True, max_length=50)
    timestamp = models.DateTimeField(auto_now_add=True)
    platform_name = models.CharField(max_length=50, default=None)

    def __str__(self) -> str:
        return self.room_name
