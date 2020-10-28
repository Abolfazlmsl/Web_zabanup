from django.contrib.auth import get_user_model
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



