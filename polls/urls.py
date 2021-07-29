from django.urls import path
from rest_framework.routers import SimpleRouter

from .views import *

router = SimpleRouter()
router.register('polls/', PollModelViewSet, basename='polls')
router.register('question/', QuestionModelViewSet, basename='question')
router.register('answer-choice/', AnswerChoiceModelViewSet, basename='answer-choice')
router.register('user-answer/', UserAnswerModelViewSet, basename='user-answer')

urlpatterns = [
    path('', all_polls),
    path('question/', all_question),
    ]

urlpatterns += router.urls
