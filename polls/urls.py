from django.urls import path
from rest_framework.routers import SimpleRouter
from .views import *

router = SimpleRouter()
router.register('api/poll', PollModelViewSet)
router.register('api/question', QuestionModelViewSet)
router.register('api/answer_choice', AnswerChoiceModelViewSet)
router.register('api/user_answer', UserAnswerModelViewSet)

urlpatterns = [
    path('', main, name='main'),
    path('poll/', all_polls, name='poll'),
    path('poll_create/', poll_create, name='poll_create'),
    path('question/', all_question, name='question'),
    path('question_create/', question_create, name='question_create'),
    path('answer_choice/', all_answer_choice, name='answer_choice'),
    path('user_answer/', all_user_answer, name='user_answer'),
    path('users/', UserList.as_view()),
    path('users/<int:pk>/', UserDetail.as_view()),
    path('poll_list/<int:pk>', PollTempList.as_view(), name='poll_list'),
]

urlpatterns += router.urls
