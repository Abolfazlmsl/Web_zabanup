from django.urls import path, include
from . import views
urlpatterns = [
    path('exam/', views.ExamList.as_view(), name='ExamList'),
]
