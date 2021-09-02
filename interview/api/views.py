from rest_framework.permissions import IsAdminUser
from ..models import Category, Question, Choice, Answer
from .permissions import IsStartDateBegin
from .serializers import (
    CategoryModelSerializer,
    QuestionModelSerializer,
    QuestionCreateModelSerializer,
    ChoiceModelSerializer,
    AnswerModelSerializer,
)
from rest_framework import generics


class CategoryListApiView(generics.ListAPIView):
    serializer_class = CategoryModelSerializer
    queryset = Category.objects.all()


class CategoryCreateApiView(generics.ListCreateAPIView):
    serializer_class = CategoryModelSerializer
    queryset = Category.objects.all()
    permission_classes = (IsAdminUser,)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class CategoryUpdateApiView(generics.RetrieveUpdateAPIView):
    serializer_class = CategoryModelSerializer
    queryset = Category.objects.all()
    permission_classes = (IsAdminUser, IsStartDateBegin)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class CategoryDestroyApiView(generics.DestroyAPIView):
    serializer_class = CategoryModelSerializer
    queryset = Category.objects.all()
    permission_classes = (IsAdminUser, IsStartDateBegin)
    lookup_url_kwarg = 'pk'


class QuestionListApiView(generics.ListAPIView):
    serializer_class = QuestionModelSerializer

    def get_queryset(self):
        queryset = Question.objects.filter(
            category=Category.objects.get(pk=self.kwargs['pk']))
        return queryset


class QuestionCreateApiView(generics.ListCreateAPIView):
    serializer_class = QuestionCreateModelSerializer

    def perform_create(self, serializer):
        serializer.save(category=Category.objects.get(pk=self.kwargs['pk']))

    def get_queryset(self):
        return Question.objects.filter(category=Category.objects.get(pk=self.kwargs['pk']))


class QuestionUpdateApiView(generics.RetrieveUpdateAPIView):
    serializer_class = QuestionCreateModelSerializer
    queryset = Question.objects.all()
    lookup_url_kwarg = 'q_pk'


class QuestionDestroyApiView(generics.ListAPIView, generics.DestroyAPIView):
    serializer_class = QuestionModelSerializer

    def get_queryset(self):
        return Question.objects.filter(pk=self.kwargs['q_pk'])


class ChoiceList(generics.ListCreateAPIView):

    serializer_class = ChoiceModelSerializer

    def get_queryset(self):
        return Question.objects.filter(pk=self.kwargs['q_pk'])
# #
# #
# # class AnswerList(generics.ListCreateAPIView):
# #
# #     queryset = Answer.objects.all()
# #     serializer_class = AnswerModelSerializer
