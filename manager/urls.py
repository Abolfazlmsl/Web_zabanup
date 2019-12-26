from django.urls import path
from . import views

app_name = 'manager'
urlpatterns = [
    path('login/', views.login_view, name='LoginView'),
    path('', views.index, name='IndexView'),
    path('logout/', views.logout_view, name='LogOutView'),
    path('taken_exam/', views.user_answer_list, name='UserAnswer'),
    path('user/', views.user_list, name='UserList'),
    path('user/<int:pk>/', views.user_detail, name='UserDetail'),
    path('user/edit/<int:pk>/', views.user_edit, name='UserEdit'),
    path('exam/', views.exam_list, name='ExamList'),
    path('exam/create/', views.exam_create, name='ExamCreate'),
    path('exam/<int:pk>/', views.exam_edit, name='ExamEdit'),
    path('ticket/send/', views.send_ticket, name='SendTicket'),
    path('ticket/', views.ticket, name='Ticket'),
    path('ticket/<int:pk>/', views.ticket_history, name='TicketHistory'),
    path('reading/', views.reading_list, name='ReadingList'),
    path('reading/create/', views.reading_create, name='ReadingCreate'),
    path('reading/<int:pk>/', views.reading_detail, name='ReadingDetail'),
    path('reading/edit/<int:pk>/', views.reading_edit, name='ReadingEdit'),
    path('book/', views.book_list, name='BookList'),

]

