from django.contrib.auth.views import LoginView, LogoutView
from django.urls import path

from .views import (
    CategoryListView,
    CategoryDetailView,
    CategoryCreateView,
    CategoryDeleteView,
    CategoryUpdateView,

    QuestionDetailView,
    # question_update,
    QuestionCreateView,
    QuestionUpdateView,
    QuestionDeleteView,

    ChoiceCreateView,


    AnswerListView,
    AnswerCreateView,
    # answer_create,
    PollCreateView,
    poll_create,
)

urlpatterns = [
    path('', CategoryListView.as_view(), name='list'),
    path('interview/create/', CategoryCreateView.as_view(), name='category_create'),
    path('interview/update/<pk>/', CategoryUpdateView.as_view(), name='category_update'),
    path('interview/delete/<pk>/', CategoryDeleteView.as_view(), name='category_delete'),
    path('interview/<pk>/', CategoryDetailView.as_view(), name='category_detail'),

    path('question/create/', QuestionCreateView.as_view(), name='q_create'),
    path('question/update/<pk>/', QuestionUpdateView.as_view(), name='q_update'),
    path('question/delete/<pk>/', QuestionDeleteView.as_view(), name='q_delete'),
    path('question/<pk>/', QuestionDetailView.as_view(), name='q_detail'),

    path('answer/', AnswerListView.as_view(), name='answer_list'),
    path('answer/create/', AnswerCreateView.as_view(), name='answer_create'),

    path('choice/create/', ChoiceCreateView.as_view(), name='choice_create'),

    path('user/', LoginView.as_view(template_name='interview/user/user.html'), name='user'),
    path('exit/', LogoutView.as_view(template_name='interview/user/exit.html'), name='exit'),

    path('poll/create', poll_create, name='poll_create'),
]