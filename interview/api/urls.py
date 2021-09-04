from django.urls import path
from .views import (
    CategoryList,
    CategoryCreate,
    CategoryUpdate,
    CategoryDestroy,

    QuestionList,
    QuestionCreate,
    QuestionUpdate,
    QuestionDestroy,

    ChoiceList,
    ChoiceDestroy,

    AnswerNumberCreate,

    AnswerCreate,
)

from django.views.generic import TemplateView
from rest_framework.schemas import get_schema_view

urlpatterns = [
    path('', CategoryList.as_view(), name='api_list'),
    path('create/', CategoryCreate.as_view(), name='api_create'),
    path('<pk>/update/', CategoryUpdate.as_view(), name='api_update'),
    path('<pk>/delete/', CategoryDestroy.as_view(), name='api_delete'),

    path('<pk>/detail/', QuestionList.as_view(), name='api_q_list'),
    path('<pk>/create/', QuestionCreate.as_view(), name='api_q_create'),
    path('<pk>/<q_pk>/update/', QuestionUpdate.as_view(), name='api_q_update'),
    path('<pk>/<q_pk>/delete/', QuestionDestroy.as_view(), name='api_q_delete'),

    path('<pk>/<q_pk>/', ChoiceList.as_view(), name='api_choice_list'),
    path('<pk>/<q_pk>/<c_pk>/delete', ChoiceDestroy.as_view(), name='api_choice_delete'),

    path('answer/<pk>/create/', AnswerNumberCreate.as_view(), name='api_answer_number_create'),
    path('answer/<an_pk>/<pk>/<q_pk>/create/', AnswerCreate.as_view(), name='answer_create'),

    path('openapi', get_schema_view(
        title="Interview",
        description="API for interview",
        version="1.0.0"
    ), name='openapi-schema'),

    path('swagger-ui/', TemplateView.as_view(
        template_name='interview/doc_api/swagger-ui.html',
        extra_context={'schema_url': 'openapi-schema'}
    ), name='swagger-ui'),

    path('redoc/', TemplateView.as_view(
        template_name='interview/doc_api/redoc.html',
        extra_context={'schema_url': 'openapi-schema'}
    ), name='redoc'),
]
