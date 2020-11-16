from django.contrib.auth import get_user_model
from rest_framework import serializers
from core import models


class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Book
        fields = '__all__'


class QuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Question
        fields = '__all__'


class ExamSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Exam
        fields = '__all__'
        depth = 1


class ReadingSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Reading
        fields = '__all__'


class ReadingWithQuestionsSerializer(serializers.ModelSerializer):
    questions = QuestionSerializer(many=True)
    class Meta:
        model = models.Reading
        fields = '__all__'


class UserAnswerSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.UserAnswer
        fields = '__all__'
        read_only_fields = (
            'id',
            'user',
            'grade',
            'created_on'
        )


class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Category
        fields = '__all__'
