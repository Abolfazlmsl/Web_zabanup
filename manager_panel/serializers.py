from rest_framework import serializers
from django.contrib.auth import get_user_model
from core import models


class UserSerializer(serializers.ModelSerializer):
    """Serialize user model"""

    class Meta:
        model = get_user_model()
        fields = (
            'id',
            'email',
            'name',
            'phone_number',
            'national_code',
            'is_foreign_people',
            'bank_card_number'
        )
        read_only_fields = ('id',)


class BookSerializer(serializers.ModelSerializer):
    """Serialize book model"""

    class Meta:
        model = models.Book
        fields = '__all__'
        read_only_fields = ('id', 'test_taken', 'created_on')


class ExamCategorySerializer(serializers.ModelSerializer):
    """Serialize exam model"""

    class Meta:
        model = models.ExamCategory
        fields = '__all__'
        read_only_fields = ('id',)


class ExamSerializer(serializers.ModelSerializer):
    """Serialize exam model"""

    class Meta:
        model = models.Exam
        fields = '__all__'
        read_only_fields = ('id',)