from django.contrib.auth.models import User
from rest_framework import serializers
from Reading import models


class ExamDetailSerializers(serializers.ModelSerializer):
    passage = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = models.Exam
        fields = [
            'id',
            'book',
            'category',
            'difficulty',
            'image',
            'passage',
        ]
        depth = 3

    def get_passage(self, obj):
        return obj.get_api_passage()


class ExamSerializers(serializers.ModelSerializer):

    class Meta:
        model = models.Exam
        fields = [
            'id',
            'book',
            'category',
            'difficulty',
            'image',
        ]


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Profile
        fields = '__all__'


class UserAnswerListSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.UserAnswer
        fields = [
            'id',
            'grade',
            'user',
            'exam',
            'time',
        ]


class UserAnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.UserAnswer
        fields = '__all__'


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Comment
        fields = '__all__'


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'password', 'username', 'first_name', 'last_name', 'email')

#
