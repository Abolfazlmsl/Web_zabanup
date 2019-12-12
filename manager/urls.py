from django.urls import path
from . import views

app_name = 'manager'
urlpatterns = [
    path('login/', views.login_view, name='LoginView'),
    path('', views.index, name='IndexView'),
    path('logout/', views.logout_view, name='LogOutView'),
    path('taken_exams/', views.user_answer_list, name='UserAnswer'),
    path('users/', views.user_list, name='UserList'),
    path('users/<int:pk>/', views.user_detail, name='UserDetail'),
    path('users/edit/<int:pk>/', views.user_edit, name='UserEdit'),
    path('exams/', views.exam_list, name='ExamList'),
    path('exams/create/', views.exam_create, name='ExamCreate'),
    path('exams/<int:pk>/', views.exam_edit, name='ExamEdit'),
    path('ticket/send/', views.send_ticket, name='SendTicket'),
    path('ticket/', views.ticket, name='Ticket'),
    path('ticket/<int:pk>/', views.ticket_history, name='TicketHistory'),
]

