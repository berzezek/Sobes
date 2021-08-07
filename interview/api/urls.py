from django.urls import path
from .views import CategoryDetail, CategoryList, CategoryDestroy, CategoryCreate

urlpatterns = [
    path(r'', CategoryList.as_view(), name='category_list'),
    path(r'create/', CategoryCreate.as_view(), name='category_create'),
    path(r'<int:pk>/', CategoryDetail.as_view(), name='category_detail'),
    path(r'<int:pk>/delete', CategoryDestroy.as_view(), name='category_delete'),
    # path('question/', QuestionList.as_view(), name='question_list'),
    # path('choice/', ChoiceList.as_view()),
    # path('answer/', AnswerList.as_view()),
    # path('docs/', include_docs_urls(title='My API title'))
]
