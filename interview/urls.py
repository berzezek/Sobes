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
    # AnswerCreateView,
    get_name,
)

urlpatterns = [
    path('', CategoryListView.as_view(), name='list'),
    path('interview/create/', CategoryCreateView.as_view(), name='category_create'),
    path('interview/<pk>/update/', CategoryUpdateView.as_view(), name='category_update'),
    path('interview/<pk>/delete/', CategoryDeleteView.as_view(), name='category_delete'),
    path('interview/<pk>/', CategoryDetailView.as_view(), name='category_detail'),

    path('interview/<pk>/create/', QuestionCreateView.as_view(), name='q_create'),
    path('interview/<pk>/<q_pk>/update/', QuestionUpdateView.as_view(), name='q_update'),
    path('interview/<pk>/<q_pk>/delete/', QuestionDeleteView.as_view(), name='q_delete'),
    path('interview/<pk>/<q_pk>/', QuestionDetailView.as_view(), name='q_detail'),

    # path('answer/', AnswerListView.as_view(), name='answer_list'),
    path('answer/search/', AnswerListView.as_view(), name='answer_search'),
    path('answer/create/', get_name, name='answer_create'),
    # path('answer/create/', AnswerCreateView.as_view(), name='answer_create'),

    path('interview/<pk>/<q_pk>/create/', ChoiceCreateView.as_view(), name='choice_create'),

    path('user/', LoginView.as_view(template_name='interview/user/user.html'), name='user'),
    path('exit/', LogoutView.as_view(template_name='interview/user/exit.html'), name='exit'),

]