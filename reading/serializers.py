from django.contrib.auth import get_user_model
from rest_framework import serializers
from core import models

class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Book
        fields = '__all__'
