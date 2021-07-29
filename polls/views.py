from django.shortcuts import render
from django.contrib.auth.models import User
from rest_framework.viewsets import ModelViewSet
from .serializers import *
from django.http import Http404
from .models import *
from .permissions import IsOwnerOrReadOnly


class PollModelViewSet(ModelViewSet):
    """Опросы"""
    queryset = Poll.objects.all()
    serializer_class = PollSerializer
    permission_class = IsOwnerOrReadOnly


class QuestionModelViewSet(ModelViewSet):
    """Вопросы"""
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer
    permission_class = IsOwnerOrReadOnly


class AnswerChoiceModelViewSet(ModelViewSet):
    """Варианты ответов"""
    queryset = AnswerChoice.objects.all()
    serializer_class = AnswerChoiceSerializer
    permission_class = IsOwnerOrReadOnly


class UserAnswerModelViewSet(ModelViewSet):
    """Ответы"""
    queryset = UserAnswer.objects.all()
    serializer_class = UserAnswerSerializer


def all_polls(request):
    return render(request, 'polls/polls.html')


def all_question(request):
    return render(request, 'polls/question.html')


def all_user_answer(request):
    return render(request, 'polls/user-answers.html')
