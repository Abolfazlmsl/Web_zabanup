from django.urls import path, include
from rest_framework.routers import DefaultRouter

from . import views

app_name = 'user'
router = DefaultRouter()
router.register('user-answer', views.UserAnswerViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('create/', views.CreateUserView.as_view(), name='create'),
    path('me/', views.ManageUserView.as_view(), name='me'),
    path('verify-user/', views.UserPhoneRegisterAPIView.as_view(), name='verify-user'),
    path('change-password/', views.ChangePasswordView.as_view(), name='change-password'),
]