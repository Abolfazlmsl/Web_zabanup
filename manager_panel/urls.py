from django.urls import path, include
from rest_framework.routers import DefaultRouter

from . import views

app_name = 'manager'

router = DefaultRouter()
router.register('user', views.ManagerUserViewSet)
router.register('book', views.ManagerBookViewSet)
router.register('exam-category', views.ManagerExamCategoryViewSet)
router.register('exam', views.ManagerExamViewSet)
router.register('reading', views.ManagerReadingViewSet)
router.register('question', views.ManagerQuestionViewSet)
router.register('answer', views.ManagerAnswerViewSet)
router.register('user-answer', views.ManagerUserAnswerViewSet)
router.register('comment', views.ManagerCommentViewSet)
router.register('ticket', views.ManagerCommentViewSet)
router.register('ticket-message', views.ManagerCommentViewSet)


urlpatterns = [
    path('info/', views.ManagerInfoView.as_view(), name='ManagerInfo'),
    path('', include(router.urls)),
]
