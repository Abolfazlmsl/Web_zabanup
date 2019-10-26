from django.contrib.auth.models import User
from django.db.models import Q
from rest_framework import generics
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAdminUser, IsAuthenticatedOrReadOnly
from Reading import models
from . import serializers


class ExamList(generics.ListCreateAPIView):
    # permission_classes = (IsAdminUser, IsAuthenticatedOrReadOnly)

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


class ExamDetail(generics.RetrieveAPIView):
    queryset = models.Exam.objects.all()
    serializer_class = serializers.ExamSerializers


class PassageList(generics.ListAPIView):
    serializer_class = serializers.PassageSerializer

    def get_queryset(self):
        query = models.Passage.objects.all()
        exam_id = self.request.GET.get("exam_id")
        if exam_id is not None:
            exam = models.Exam.objects.get(id=exam_id)
            query = query.filter(exam=exam)

        return query


class PassageDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = models.Passage.objects.all()
    serializer_class = serializers.PassageSerializer


class QuestionList(generics.ListCreateAPIView):
    serializer_class = serializers.QuestionSerializer

    def get_queryset(self):
        query = models.Question.objects.all()
        passage_id = self.request.GET.get("passage_id")
        if passage_id is not None:
            passage = models.Passage.objects.get(id=passage_id)
            query = query.filter(passage=passage)
        return query


class QuestionDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = models.Question.objects.all()
    serializer_class = serializers.QuestionSerializer


class AnswerList(generics.ListAPIView):
    serializer_class = serializers.AnswerSerializer

    def get_queryset(self):
        query = models.Answer.objects.all()
        question_id = self.request.GET.get("question_id")
        if question_id is not None:
            question = models.Passage.objects.get(id=question_id)
            query = query.filter(question=question)
        return query


class AnswerDetail(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = serializers.AnswerSerializer
    queryset = models.Answer.objects.all()


class UserAnswerList(generics.ListAPIView):
    serializer_class = serializers.UserAnswerSerializer

    def get_queryset(self):
        query = models.UserAnswer.objects.all()

        exam = self.request.GET.get('exam')
        user = self.request.GET.get('user')

        if exam is not None:
            query = query.filter(exam=exam)
        if user is not None:
            query = query.filter(user=user)

        return query

#
# class UserAnswerCreate(generics.CreateAPIView):
#     serializer_class = serializers.UserAnswerSerializer
#
#     def get_queryset(self):




class UserAnswerDetail(generics.RetrieveAPIView):
    queryset = models.UserAnswer.objects.all()
    serializer_class = serializers.UserAnswerSerializer


class UserList(generics.ListCreateAPIView):
    serializer_class = serializers.UserSerializer
    queryset = User.objects.filter(is_superuser=False)


class UserDetail(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = serializers.UserSerializer
    queryset = User.objects.filter(is_superuser=False)


class CommentList(generics.ListCreateAPIView):
    serializer_class = serializers.CommentSerializer
    queryset = models.Comment.objects.all()


class CommentDetail(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = serializers.CommentSerializer
    queryset = models.Comment.objects.all()




