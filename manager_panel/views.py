from django.contrib.auth import get_user_model
from rest_framework import generics, viewsets, mixins
from rest_framework.pagination import PageNumberPagination
from rest_framework_simplejwt.authentication import JWTAuthentication

from core import models
from manager_panel import serializers, permissions


class StandardResultsSetPagination(PageNumberPagination):
    page_size = 20
    page_size_query_param = 'page_size'
    max_page_size = 100


class ManagerInfoView(generics.RetrieveUpdateAPIView):
    """Show detailed of manager user"""
    serializer_class = serializers.UserSerializer
    authentication_classes = (JWTAuthentication,)
    permission_classes = (permissions.IsManager,)
    queryset = get_user_model().objects.all()

    def get_object(self):
        """Retrieve anr return authenticated user"""
        return self.request.user


class ManagerUserViewSet(viewsets.GenericViewSet,
                         mixins.ListModelMixin,
                         mixins.RetrieveModelMixin):
    """user for manager"""

    serializer_class = serializers.UserSerializer
    authentication_classes = (JWTAuthentication,)
    permission_classes = (permissions.IsManager,)
    pagination_class = StandardResultsSetPagination
    queryset = get_user_model().objects.all()

    def get_queryset(self):
        """Filter user that doesn't show admin or staff"""
        return self.queryset.filter(
            is_superuser=False, is_staff=False
        ).exclude(groups__name='Manager')


class ManagerBookViewSet(viewsets.ModelViewSet):
    """Manage books in database"""

    serializer_class = serializers.BookSerializer
    authentication_classes = (JWTAuthentication,)
    permission_classes = (permissions.IsManager,)
    pagination_class = StandardResultsSetPagination
    queryset = models.Book.objects.all()


class ManagerExamCategoryViewSet(viewsets.ModelViewSet):
    """Manage exams in database"""

    serializer_class = serializers.ExamCategorySerializer
    authentication_classes = (JWTAuthentication,)
    permission_classes = (permissions.IsManager,)
    pagination_class = StandardResultsSetPagination
    queryset = models.ExamCategory.objects.all()


class ManagerExamViewSet(viewsets.ModelViewSet):
    """Manage exams in database"""

    serializer_class = serializers.ExamSerializer
    authentication_classes = (JWTAuthentication,)
    permission_classes = (permissions.IsManager,)
    pagination_class = StandardResultsSetPagination
    queryset = models.Exam.objects.all()
