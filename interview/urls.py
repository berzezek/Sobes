from django.contrib.auth.views import LoginView, LogoutView
from django.urls import path

from .views import (
    CategoryListView,
    CategoryDetailView,
    CategoryCreateView,
    CategoryDeleteView,
    CategoryUpdateView,

    QuestionListView,
    QuestionDetailView,
    QuestionCreateView,
    QuestionUpdateView,
    QuestionDeleteView,

    ChoiceCreateView,
    ChoiceDeleteView,

    AnswerListView,
    AnswerCreateView,

)

urlpatterns = [
    path('', CategoryListView.as_view(), name='list'),
    path('interview/create/', CategoryCreateView.as_view(), name='category_create'),
    path('interview/<pk>/update/', CategoryUpdateView.as_view(), name='category_update'),
    path('interview/<pk>/delete/', CategoryDeleteView.as_view(), name='category_delete'),
    path('interview/<pk>/', CategoryDetailView.as_view(), name='category_detail'),

    path('question/<pk>/', QuestionListView.as_view(), name='q_list'),
    path('question/<pk>/create/', QuestionCreateView.as_view(), name='q_create'),
    path('question/<pk>/<q_pk>/update/', QuestionUpdateView.as_view(), name='q_update'),
    path('question/<pk>/<q_pk>/delete/', QuestionDeleteView.as_view(), name='q_delete'),
    path('question/<pk>/<q_pk>/', QuestionDetailView.as_view(), name='q_detail'),

    path('answer/', AnswerListView.as_view(), name='answer_list'),
    path('answer/search/', AnswerListView.as_view(), name='answer_search'),
    path('answer/<pk>/create/', AnswerCreateView.as_view(), name='answer_create'),

    path('choice/<pk>/<q_pk>/create/', ChoiceCreateView.as_view(), name='choice_create'),
    path('choice/<pk>/<q_pk>/<c_pk>/delete/', ChoiceDeleteView.as_view(), name='choice_delete'),

    path('user/', LoginView.as_view(template_name='interview/user/user.html'), name='user'),
    path('exit/', LogoutView.as_view(template_name='interview/user/exit.html'), name='exit'),
]