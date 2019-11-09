from django.urls import path
from . import views

app_name = 'manager'
urlpatterns = [
    path('login/', views.login_view, name='LoginView'),
    path('', views.index, name='IndexView'),
    path('logout/', views.logout_view, name='LogOutView'),
    path('exams/', views.exam_list, name='ExamList'),
]
