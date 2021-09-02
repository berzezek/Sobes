from django.urls import path
from .views import (
    CategoryListApiView,
    CategoryCreateApiView,
    CategoryUpdateApiView,
    CategoryDestroyApiView,

    QuestionListApiView,
    QuestionCreateApiView,
    QuestionUpdateApiView,
    QuestionDestroyApiView,
)

from django.views.generic import TemplateView
from rest_framework.schemas import get_schema_view

urlpatterns = [
    path('', CategoryListApiView.as_view(), name='api_list'),
    path('create/', CategoryCreateApiView.as_view(), name='api_create'),
    path('<pk>/update/', CategoryUpdateApiView.as_view(), name='api_update'),
    path('<pk>/delete/', CategoryDestroyApiView.as_view(), name='api_delete'),

    path('<pk>/detail/', QuestionListApiView.as_view(), name='api_q_list'),
    path('<pk>/create/', QuestionCreateApiView.as_view(), name='api_q_create'),
    path('<pk>/<q_pk>/update/', QuestionUpdateApiView.as_view(), name='api_q_update'),
    path('<pk>/<q_pk>/delete/', QuestionDestroyApiView.as_view(), name='api_q_delete'),

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
