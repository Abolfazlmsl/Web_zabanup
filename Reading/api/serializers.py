from django.contrib.auth.models import User
from rest_framework import serializers
from Reading import models


class PassageSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Answer
        fields = '__all__'


class ExamSerializers(serializers.ModelSerializer):
    # passage = serializers.SerializerMethodField(read_only=True)
    # question = serializers.SerializerMethodField(read_only=True)
    # answer = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = models.Exam
        fields = [
            'id',
            'category',
            # 'passage',
            # 'question',
            # 'answer',
            'book',
        ]
        depth = 4

    # def get_passage(self, obj):
    #     return obj.get_api_passage()

    # def get_question(self, obj):
    #     return obj.get_api_question()
    #
    # def get_answer(self, obj):
    #     return obj.get_api_answer()


class QuestionSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Question
        fields = '__all__'


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Profile
        fields = '__all__'



class AnswerSerializer(serializers.ModelSerializer):
    # question = serializers.SerializerMethodField(read_only=True)
    passage = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = models.Answer
        fields = [
            'passage',
            'question',
            'id',
            'text',
        ]
        depth = 3
    #
    # def get_question(self, obj):
    #     return obj.get_api_question()

    def get_passage(self, obj):
        return obj.get_api_passage()


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

