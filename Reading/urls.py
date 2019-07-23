from django.contrib import admin
from django.urls import path, include, re_path
from django.conf.urls import url
from . import views

app_name = 'Reading'
urlpatterns = [
    path('', views.home, name='home'),
    path('signup/', views.signup_view, name='SignUp'),
    path('login/', views.login_view, name='Login'),
    path('logout/', views.logout_view, name='LogOut'),
    path('changepassword/', views.change_password, name='changePassword'),
    path('Reading/', views.reading, name='Reading'),
    url(r'^Reading/(?P<passage_id>[0-9]+)/$', views.passage_body, name='passage_body'),
    url(r'^Reading/(?P<passage_id>[0-9]+)/submit$', views.submit, name='submit'),

]
