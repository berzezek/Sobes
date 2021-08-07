from django.urls import path

from .views import CategoryListView, CategoryDetailView, category_create, QuestionDetailView

urlpatterns = [
    path('', CategoryListView.as_view(), name='list'),
    path('interview/<slug>/', CategoryDetailView.as_view(), name='category_detail'),
    path('interview/<slug>/<q_slug>', QuestionDetailView.as_view(), name='question_detail'),

    path('create/', category_create, name='create'),
]