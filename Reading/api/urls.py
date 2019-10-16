from django.urls import path, include
from . import views
urlpatterns = [
    path('exam/', views.ExamList.as_view(), name='ExamList'),
    path('exam/<int:pk>', views.PassageList.as_view(), name='PassageList'),
]
