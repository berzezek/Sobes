from django.urls import path
from rest_framework.routers import SimpleRouter
from .views import *


router = SimpleRouter()
router.register('api/v1/poll', PollViewSet)


urlpatterns = [
    path('', all_polls),

    path('poll/all/', PollListView.as_view()),
    path('question/all/', QuestionListView.as_view()),

    path('poll/create/', PollCreateView.as_view()),
    path('question/create/', QuestionCreateView.as_view()),
    path('useranswer/create/', UserAnswerCreateView.as_view()),

    path('poll/detail/<int:pk>', PollRUDView.as_view()),
    path('question/detail/<int:pk>', PollRUDView.as_view()),

]

urlpatterns += router.urls