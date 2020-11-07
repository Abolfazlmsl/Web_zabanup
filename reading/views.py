from django.contrib.auth import get_user_model
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from rest_framework import generics, status, viewsets, mixins
from rest_framework.generics import UpdateAPIView, get_object_or_404
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated

from core import models
from . import serializers


class BookViewSet(viewsets.GenericViewSet,
                  mixins.ListModelMixin,
                  mixins.RetrieveModelMixin):
    """ list and retrieve books """
    serializer_class = serializers.BookSerializer
    authentication_classes = (JWTAuthentication,)
    queryset = models.Book.objects.all()


class ExamViewSet(viewsets.GenericViewSet,
                  mixins.ListModelMixin,
                  mixins.RetrieveModelMixin):
    """ list and retrieve exams """
    filter_backends = [
        DjangoFilterBackend,
        filters.OrderingFilter,
        filters.SearchFilter
    ]
    # ordering_fields = ['rate',]
    search_fields = ('book',)
    serializer_class = serializers.ExamSerializer
    authentication_classes = (JWTAuthentication,)
    queryset = models.Exam.objects.all()


class ReadingViewSet(viewsets.GenericViewSet,
                        mixins.ListModelMixin,
                        mixins.RetrieveModelMixin):
    """ list and retrieve readings """
    filter_backends = [
        DjangoFilterBackend,
        filters.OrderingFilter,
        filters.SearchFilter
    ]
    # ordering_fields = ['rate',]
    search_fields = ('exam',)
    serializer_class = serializers.ReadingSerializer
    authentication_classes = (JWTAuthentication,)
    queryset = models.Reading.objects.all()


class UserAnswerAPIView(APIView):
    serializer_class = serializers.UserAnswerSerializer
    authentication_classes = (JWTAuthentication,)
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        answers = request.data['answer']
        exam = request.data['exam']
        correct_answerlist = models.Answer.objects.filter(question__passage__exam_id=exam)
        for a in correct_answerlist:
            print(a.text)
            print(a.truth)
        print(answers)
        message = {
            'message': 'ok'
        }
        return Response(
            message,
            status=status.HTTP_201_CREATED
        )