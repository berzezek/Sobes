from django.contrib.auth.views import LoginView, LogoutView
from django.urls import path

from .views import (
    CategoryListView,
    CategoryDetailView,
    CategoryCreateView,
    CategoryDeleteView,
    CategoryUpdateView,

    QuestionCreateView,
    question_update,
    choice_create,
    QuestionDetailView,
    AnswerListView,
    answer_create,
    PollCreateView,
)

urlpatterns = [
    path('', CategoryListView.as_view(), name='list'),
    path('interview/create/', CategoryCreateView.as_view(), name='category_create'),
    path('interview/delete/<pk>', CategoryDeleteView.as_view(), name='category_delete'),
    path('interview/update/<pk>', CategoryUpdateView.as_view(), name='category_update'),
    path('interview/<pk>/', CategoryDetailView.as_view(), name='category_detail'),

    # path('interview/create/', category_create, name='create'),
    # path('interview/update/<pk>', category_update, name='category_update'),
    # path('interview/delete/<pk>', category_delete, name='category_delete'),



    path('interview/<pk>/<q_pk>', QuestionDetailView.as_view(), name='question_detail'),

    path('answer/', AnswerListView.as_view(), name='answer_list'),
    path('answer/create/', answer_create, name='answer_create'),


    path('question/create/', QuestionCreateView.as_view(), name='q_create'),
    path('question/update/<pk>/', question_update, name='q_update'),
    path('question/delete/<pk>/', question_update, name='q_delete'),
    path('c_create/', choice_create, name='c_create'),
    path('user/', LoginView.as_view(template_name='interview/user/user.html'), name='user'),
    path('exit/', LogoutView.as_view(template_name='interview/user/exit.html'), name='exit'),

    path('poll/create', PollCreateView.as_view(), name='poll_create')
]