from django.urls import path
from django.conf.urls import url
from . import views
from django.conf import settings
from django.conf.urls.static import static

# Urls of app

app_name = 'Reading'
urlpatterns = [
    path('', views.index, name='Index'),
    path('book/', views.book, name='Book'),
    path('book/<int:pk>/', views.exam, name='Exam'),
    path('signup/', views.signup_view, name='SignUp'),
    path('login/', views.login_view, name='Login'),
    path('logout/', views.logout_view, name='LogOut'),
    url(r'^Reading/(?P<exam_id>[0-9]+)/$', views.passage_body, name='passage_body'),
    url(r'^Reading/(?P<exam_id>[0-9]+)/submit$', views.submit, name='submit'),

]


if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
