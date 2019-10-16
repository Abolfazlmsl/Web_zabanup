from django.urls import path, include
from . import views
urlpatterns = [
    path('exam/', views.ExamList.as_view(), name='ExamList'),
    path('passage/', views.PassageList.as_view(), name='PassageList'),
    path('question/', views.QuestionList.as_view(), name='QuestionList'),
    path('answer/', views.AnswerList.as_view(), name='AnswerList'),
    path('user/', views.UserList.as_view(), name='UserList'),
    path('user/<int:pk>/', views.UserDetail.as_view(), name='UserDetail'),
]
