from django.urls import path, include
from rest_framework.routers import DefaultRouter

from . import views

app_name = 'manager'

router = DefaultRouter()
router.register('user', views.ManagerUserViewSet)
router.register('book', views.ManagerBookViewSet)
router.register('exam-category', views.ManagerExamCategoryViewSet)
router.register('exam', views.ManagerExamViewSet)


urlpatterns = [
    path('', include(router.urls)),
]
