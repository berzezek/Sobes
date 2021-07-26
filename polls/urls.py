from django.urls import path, include
from rest_framework.authtoken.views import obtain_auth_token
from rest_framework.routers import SimpleRouter
from .views import PollViewSet, QuestionViewSet, all_polls, create_poll, QuestionView

router = SimpleRouter()
router.register('api/poll', PollViewSet)
router.register('api/question', QuestionViewSet)

urlpatterns = [
    path('', all_polls),
    path('qu-all/', QuestionView.as_view()),

    path('create-poll/', create_poll),

    path('auth', include('djoser.urls')),
    path('auth/token', obtain_auth_token, name='token')

    # path('api-auth/', include('rest_framework.urls', namespace='rest_framework'))
]

urlpatterns += router.urls
