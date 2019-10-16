from django.db.models import Q
from django.shortcuts import get_list_or_404
from rest_framework import generics
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

