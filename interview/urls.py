from django.contrib.auth.views import LoginView, LogoutView
from django.urls import path

from .views import (
    CategoryListView,
    CategoryDetailView,
    category_create,
    category_update,
    category_delete,
    question_create,
    question_update,
    choice_create,
    QuestionDetailView,
    AnswerListView,
)

urlpatterns = [
    path('', CategoryListView.as_view(), name='list'),

    path('interview/create/', category_create, name='create'),
    path('interview/update/<pk>', category_update, name='category_update'),
    path('interview/delete/<pk>', category_delete, name='category_delete'),

    path('interview/<pk>/', CategoryDetailView.as_view(), name='category_detail'),

    path('interview/<pk>/<q_pk>', QuestionDetailView.as_view(), name='question_detail'),

    path('answer/', AnswerListView.as_view(), name='answer_list'),


    path('question/create/', question_create, name='q_create'),
    path('question/update/<pk>/', question_update, name='q_update'),
    path('c_create/', choice_create, name='c_create'),
    path('user/', LoginView.as_view(template_name='interview/user/user.html'), name='user'),
    path('exit/', LogoutView.as_view(template_name='interview/user/exit.html'), name='exit'),
]