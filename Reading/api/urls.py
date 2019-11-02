from django.urls import path, include
from . import views
from rest_framework_simplejwt import views as jwt_views

urlpatterns = [
    path('exam/', views.ExamList.as_view(), name='ExamList'),
    path('exam/<int:pk>/', views.ExamDetail.as_view(), name='ExamDetail'),
    path('user_answer/', views.UserAnswerList.as_view(), name='AnswerList'),
    path('user_answer/<int:pk>/', views.UserAnswerDetail.as_view(), name='UserAnswerDetail'),
    path('profile/<int:user>/', views.ProfileDetail.as_view(), name='ProfileDetail'),
    path('user/', views.UserList.as_view(), name='UserList'),
    path('user/<int:pk>/', views.UserDetail.as_view(), name='UserDetail'),
    path('token/', jwt_views.TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', jwt_views.TokenRefreshView.as_view(), name='token_refresh'),
]
