from django.shortcuts import render
from django.contrib.auth.models import User
from rest_framework.viewsets import ModelViewSet
from rest_framework import generics, views, response, status, permissions
from .serializers import *
from django.http import Http404
from .models import *
from .permissions import IsOwnerOrReadOnly


class UserList(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class UserDetail(generics.RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class PollList(generics.ListCreateAPIView):
    """Для опросов"""
    queryset = Poll.objects.all()
    serializer_class = PollSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly,
                          IsOwnerOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(owner_poll=self.request.user)


class PollDetail(generics.RetrieveUpdateDestroyAPIView):

    queryset = Poll.objects.all()
    serializer_class = PollSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]


class QuestionList(generics.ListCreateAPIView):
    """Для вопросов"""
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]


class QuestionDetail(generics.RetrieveUpdateDestroyAPIView):

    queryset = Question.objects.all()
    serializer_class = QuestionSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]


class AnswerChoiceList(generics.ListCreateAPIView):
    """Для вариантов ответов"""
    queryset = AnswerChoice.objects.all()
    serializer_class = AnswerChoiceSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]


class AnswerChoiceDetail(generics.RetrieveUpdateDestroyAPIView):

    # queryset = AnswerChoice.objects.select_related('answer')
    queryset = AnswerChoice.objects.all()
    serializer_class = AnswerChoiceSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]


class UserAnswerList(generics.ListCreateAPIView):
    """Для ответов пользователя"""
    queryset = UserAnswer.objects.all()
    serializer_class = UserAnswerSerializer


class UserAnswerDetail(generics.RetrieveUpdateDestroyAPIView):

    queryset = UserAnswer.objects.all()
    serializer_class = UserAnswerSerializer


def all_polls(request):
    return render(request, 'polls/index.html')



