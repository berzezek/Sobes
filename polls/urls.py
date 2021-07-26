from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from .views import *


urlpatterns = [
    path('polls/', PollList.as_view()),
    path('polls/<int:pk>/', PollDetail.as_view()),

    path('question/', QuestionList.as_view()),
    path('question/<int:pk>/', QuestionList.as_view()),

    path('users/', UserList.as_view()),
    path('users/<int:pk>/', UserDetail.as_view()),

    path('answerchoice/', AnswerChoiceList.as_view()),
    path('answerchoice/<int:pk>/', AnswerChoiceDetail.as_view()),

    path('user-answer/', UserAnswerList.as_view()),
    path('user-answer/<int:pk>/', UserAnswerDetail.as_view()),

    # path('', all_polls),

]

urlpatterns = format_suffix_patterns(urlpatterns)
