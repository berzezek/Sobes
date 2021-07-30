from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet
from rest_framework.generics import RetrieveAPIView
from .serializers import *
from .models import *


class UserDetail(RetrieveAPIView):
    """Для авторизации"""
    queryset = User.objects.all()
    serializer_class = UserSerializer


class PollModelViewSet(ModelViewSet):
    """Опросы"""
    queryset = Poll.objects.all()
    serializer_class = PollSerializer


class QuestionModelViewSet(ModelViewSet):
    """Вопросы"""
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer


class AnswerChoiceModelViewSet(ModelViewSet):
    """Варианты ответов"""
    queryset = AnswerChoice.objects.all()
    serializer_class = AnswerChoiceSerializer


class UserAnswerModelViewSet(ModelViewSet):
    """Ответы пользователей"""
    queryset = UserAnswer.objects.all()
    serializer_class = UserAnswerSerializer


def main(request):
    return render(request, 'polls/index.html')


def all_polls(request):
    return render(request, 'polls/poll.html')


def poll_create(request):
    return render(request, 'polls/poll_create.html')


def all_question(request):
    return render(request, 'polls/question.html')


def question_create(request):
    return render(request, 'polls/question_create.html')


def all_answer_choice(request):
    return render(request, 'polls/answer_choice.html')


def all_user_answer(request):
    return render(request, 'polls/user_answer.html')
