from django.contrib.auth.models import User
from django.db.models import Q
from django.http import HttpResponse
from django.shortcuts import get_list_or_404
from rest_framework import generics
from rest_framework.response import Response

from Reading import models
from . import serializers



class ExamList(generics.ListAPIView):
    serializer_class = serializers.ExamSerializers

    def get_queryset(self):
        query = models.Exam.objects.all()

        book = self.request.GET.get('book')
        category = self.request.GET.get('category')
        difficulty = self.request.GET.get('difficulty')

        if book is not None:
            book_list = book.split(",")
            query = query.filter(
                Q(book__in=book_list)
            ).distinct()
        if category is not None:
            category_list = category.split(",")
            query = query.filter(
                Q(category__in=category_list)
            ).distinct()
        if difficulty is not None:
            difficulty_list = difficulty.split(',')
            query = query.filter(
                Q(difficulty__in=difficulty_list)
            ).distinct()
        return query


class PassageList(generics.ListAPIView):
    serializer_class = serializers.PassageSerializer

    def get_queryset(self):
        query = models.Passage.objects.all()
        exam_id = self.request.GET.get("exam_id")
        if exam_id is not None:
            exam = models.Exam.objects.get(id=exam_id)
            query = query.filter(exam=exam)

        return query


class QuestionList(generics.ListAPIView):
    serializer_class = serializers.QuestionSerializer

    def get_queryset(self):
        query = models.Question.objects.all()
        passage_id = self.request.GET.get("passage_id")
        if passage_id is not None:
            passage = models.Passage.objects.get(id=passage_id)
            query = query.filter(passage=passage)
        return query


class AnswerList(generics.ListAPIView):
    serializer_class = serializers.AnswerSerializer

    def get_queryset(self):
        query = models.Answer.objects.all()
        question_id = self.request.GET.get("question_id")
        if question_id is not None:
            question = models.Passage.objects.get(id=question_id)
            query = query.filter(question=question)
        return query


class UserList(generics.ListCreateAPIView):
    serializer_class = serializers.UserSerializer
    queryset = User.objects.filter(is_superuser=False)

    def post(self, request, *args, **kwargs):
        username = self.request.POST.get('username')
        email = self.request.POST.get('email')
        first_name = self.request.POST.get('first_name')
        last_name = self.request.POST.get('last_name')
        password = self.request.POST.get('password')

        if User.objects.filter(username=username) or User.objects.filter(email=email):
            return HttpResponse('username/email is already taken!')

        User.objects.create_user(username=username, email=email, first_name=first_name, last_name=last_name, password=password)
        return Response('Your account is successfully created')

class UserDetail(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = serializers.UserSerializer
    queryset = User.objects.filter(is_superuser=False)

    def put(self, request, *args, **kwargs):
        username = self.request.POST.get('username')
        email = self.request.POST.get('email')
        first_name = self.request.POST.get('first_name')
        last_name = self.request.POST.get('last_name')
        password = self.request.POST.get('password')

        if User.objects.filter(username=username) or User.objects.filter(email=email):
            return HttpResponse('username/email is already taken!')

        User.objects.update_user(username=username, email=email, first_name=first_name, last_name=last_name,
                                 password=password)
        return Response('Your account is successfully edited')


