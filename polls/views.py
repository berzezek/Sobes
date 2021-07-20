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


class UserAnswerRUDView(RetrieveUpdateDestroyAPIView):
    serializer_class = UserAnswerSerializers
    queryset = UserAnswer.objects.all()


class PollCreateView(CreateAPIView):
    serializer_class = PollSerializers


class QuestionCreateView(CreateAPIView):
    serializer_class = QuestionSerializers


class UserAnswerCreateView(CreateAPIView):
    serializer_class = UserAnswerSerializers


class PollListView(ListAPIView):
    queryset = Poll.objects.all()
    serializer_class = PollSerializers


class QuestionListView(ListAPIView):
    queryset = Question.objects.all()
    serializer_class = QuestionSerializers


class UserAnswerListView(ListAPIView):
    queryset = UserAnswer.objects.all()
    serializer_class = UserAnswerSerializers


class PollViewSet(ModelViewSet):
    queryset = Poll.objects.all()
    serializer_class = PollSerializers


def all_polls(request):
    return render(request, 'polls/index.html')