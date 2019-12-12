from django.urls import path
from django.conf.urls import url
from . import views
from django.conf import settings
from django.conf.urls.static import static

# Urls of app

app_name = 'student'

urlpatterns = [
    path('login/', views.login_view, name='UserLogin'),
    path('', views.panel, name='index'),
    path('edit/', views.edit_information, name='edit_information'),
    path('change_password/', views.change_password, name='changePassword'),
    path('answers/', views.answers, name='answers'),
    path('answers/<int:pk>/', views.exam_answer_detail, name='examAnswerDetail'),
    path('message/', views.messages, name='messages'),
    path('sendmessage/', views.send_messages, name='send_messages'),
    path('chat/<int:pk>/', views.chat, name='chat'),
]