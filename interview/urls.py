from django.urls import path
from .views import CategoryDetail, CategoryList, CategoryCreate, QuestionList, ChoiceList, AnswerList
# from rest_framework.documentation import include_docs_urls

urlpatterns = [
    path('', CategoryList.as_view(), name='category_list'),
    path('create/', CategoryCreate.as_view(), name='category_create'),
    path('<int:pk>', CategoryDetail.as_view(), name='category_detail'),
    path('question/', QuestionList.as_view(), name='question_list'),
    path('choice/', ChoiceList.as_view()),
    path('answer/', AnswerList.as_view()),
    # path('docs/', include_docs_urls(title='My API title'))
]
