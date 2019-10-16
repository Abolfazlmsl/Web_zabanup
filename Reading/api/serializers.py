from rest_framework import serializers
from Reading import models


class ExamSerializers(serializers.ModelSerializer):

    class Meta:
        model = models.Exam
        fields = '__all__'


class QuestionSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Question
        fields = '__all__'


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Profile
        fields = '__all__'


class PassageSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Passage
        fields = '__all__'


class AnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Answer
        fields = '__all__'


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
        model = models.User
        fields = ('id', 'password', 'username', 'first_name', 'last_name', 'email')
