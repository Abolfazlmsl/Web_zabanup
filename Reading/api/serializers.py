from rest_framework import serializers
from Reading import models


class ExamSerializers(serializers.ModelSerializer):

    class Meta:
        model = models.Exam
        fields = '__all__'
