from rest_framework import generics
from Reading import models
from . import serializers


class ExamList(generics.ListAPIView):

    queryset = models.Exam.objects.all()
    serializer_class = serializers.ExamSerializers
