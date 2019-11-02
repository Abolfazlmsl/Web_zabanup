from django.contrib.auth.models import User
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated, IsAdminUser, IsAuthenticatedOrReadOnly
from . import permissons
from Reading import models
from . import serializers


class ExamList(generics.ListAPIView):
    # permission_classes = (IsAdminUser, IsAuthenticatedOrReadOnly)

    serializer_class = serializers.ExamSerializers

    def get_queryset(self):
        query = models.Exam.objects.all()

        book = self.request.GET.get('book')
        category = self.request.GET.get('category')
        difficulty = self.request.GET.get('difficulty')

        if book is not None:
            book_list = book.split(",")
            query = query.filter(book__in=book_list)
        if category is not None:
            category_list = category.split(",")
            query = query.filter(category__in=category_list)
        if difficulty is not None:
            difficulty_list = difficulty.split(',')
            query = query.filter(difficulty__in=difficulty_list)

        return query


class ExamDetail(generics.RetrieveAPIView):
    queryset = models.Exam.objects.all()
    serializer_class = serializers.ExamDetailSerializers


class UserAnswerList(generics.ListCreateAPIView):
    permission_classes = (IsAuthenticatedOrReadOnly,)
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


class UserAnswerDetail(generics.RetrieveAPIView):
    permission_classes = (IsAuthenticatedOrReadOnly,)
    queryset = models.UserAnswer.objects.all()
    serializer_class = serializers.UserAnswerSerializer


class UserList(generics.ListCreateAPIView):
    serializer_class = serializers.UserSerializer
    queryset = User.objects.filter(is_superuser=False)


class UserDetail(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = serializers.UserSerializer
    queryset = User.objects.filter(is_superuser=False)
    permission_classes = (permissons.UserPermission,)


class ProfileList(generics.CreateAPIView):
    serializer_class = serializers.ProfileSerializer
    queryset = models.Profile.objects.all()


class ProfileDetail(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = serializers.ProfileSerializer
    lookup_field = 'user'
    queryset = models.Profile.objects.all()


class CommentList(generics.ListCreateAPIView):
    serializer_class = serializers.CommentSerializer

    def get_queryset(self):
        query = models.Comment.objects.all()

        exam = self.request.GET.get('exam')
        user = self.request.GET.get('user')

        if exam is not None:
            query = query.filter(exam=exam)
        if user is not None:
            query = query.filter(user=user)

        return query


class CommentDetail(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = serializers.CommentSerializer
    queryset = models.Comment.objects.all()
