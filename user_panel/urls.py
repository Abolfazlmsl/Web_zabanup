from django.urls import path

from . import views

app_name = 'user'

urlpatterns = [
    path('create/', views.CreateUserView.as_view(), name='create'),
    path('me/', views.ManageUserView.as_view(), name='me'),
    path('verify-user/', views.UserPhoneRegisterAPIView.as_view(), name='verify-user'),
    path('change-password/', views.ChangePasswordView.as_view(), name='change-password'),
]