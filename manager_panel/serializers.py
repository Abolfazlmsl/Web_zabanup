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


class ReadingSerializer(serializers.ModelSerializer):
    """Serialize reading model"""

    class Meta:
        model = models.Reading
        fields = '__all__'
        read_only_fields = ('id',)


class QuestionSerializer(serializers.ModelSerializer):
    """Serialize question model"""

    class Meta:
        model = models.Question
        fields = '__all__'
        read_only_fields = ('id',)


class AnswerSerializer(serializers.ModelSerializer):
    """Serialize answer model"""

    class Meta:
        model = models.Answer
        fields = '__all__'
        read_only_fields = ('id',)


class UserAnswerSerializer(serializers.ModelSerializer):
    """Serialize user answer model"""

    class Meta:
        model = models.UserAnswer
        fields = '__all__'


class CommentSerializer(serializers.ModelSerializer):
    """Serialize comment model"""

    class Meta:
        model = models.Comment
        fields = '__all__'


class TicketSerializer(serializers.ModelSerializer):
    """Serialize ticket model"""

    class Meta:
        model = models.Ticket
        fields = '__all__'


class TickerMessageSerializer(serializers.ModelSerializer):
    """Serialize ticket message model"""

    class Meta:
        model = models.TicketMessage
        fields = '__all__'
        read_only_fields = ('id', 'sender')


