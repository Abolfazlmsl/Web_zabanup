from django.urls import path, include
from . import views
from rest_framework_simplejwt import views as jwt_views

urlpatterns = [
    path('exam/', views.ExamList.as_view(), name='ExamList'),
    path('exam/<int:pk>/', views.ExamDetail.as_view(), name='ExamDetail'),
    path('passage/', views.PassageList.as_view(), name='PassageList'),
    path('passage/<int:pk>/', views.PassageDetail.as_view(), name='PassageDetail'),
    path('question/', views.QuestionList.as_view(), name='QuestionList'),
    path('question/<int:pk>/', views.QuestionDetail.as_view(), name='QuestionDetail'),
    path('answer/', views.AnswerList.as_view(), name='AnswerList'),
    path('answer/<int:pk>/', views.AnswerDetail.as_view(), name='AnswerDetail'),
    path('user_answer/', views.UserAnswerList.as_view(), name='AnswerList'),
    path('user_answer/<int:pk>/', views.UserAnswerDetail.as_view(), name='UserAnswerDetail'),
    path('user/', views.UserList.as_view(), name='UserList'),
    path('user/<int:pk>/', views.UserDetail.as_view(), name='UserDetail'),
    path('token/', jwt_views.TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', jwt_views.TokenRefreshView.as_view(), name='token_refresh'),
]
