from django.shortcuts import render
from .models import *
from rest_framework.viewsets import ModelViewSet
from rest_framework.generics import CreateAPIView, ListAPIView, RetrieveUpdateDestroyAPIView
from .serializers import PollSerializers, QuestionSerializers, UserAnswerSerializers


class PollRUDView(RetrieveUpdateDestroyAPIView):
    serializer_class = PollSerializers
    queryset = Poll.objects.all()


class QuestionRUDView(RetrieveUpdateDestroyAPIView):
    serializer_class = QuestionSerializers
    queryset = Question.objects.all()


class PollCreateView(CreateAPIView):
    serializer_class = QuestionSerializers


class QuestionCreateView(CreateAPIView):
    serializer_class = QuestionSerializers


class PollListView(ListAPIView):
    queryset = Poll.objects.all()
    serializer_class = PollSerializers


class QuestionListView(ListAPIView):
    queryset = Question.objects.all()
    serializer_class = QuestionSerializers


class PollViewSet(ModelViewSet):
    queryset = Poll.objects.all()
    serializer_class = PollSerializers


class UserAnswerCreateView(CreateAPIView):
    serializer_class = UserAnswerSerializers


def all_polls(request):
    return render(request, 'polls/index.html')