from dataclasses import field, fields
from rest_framework import serializers
from .models import *


class ViewMessageSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ("__all__")
        model = ChatModel
