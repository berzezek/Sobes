from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet
from rest_framework import generics
from .serializers import *


class QuestionView(generics.ListAPIView):
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer


class PollViewSet(ModelViewSet):
    queryset = Poll.objects.all()
    serializer_class = PollSerializer

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class QuestionViewSet(ModelViewSet):
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer


def all_polls(request):
    return render(request, 'polls/index.html')


def create_poll(request):
    return render(request, 'polls/poll-create.html')



