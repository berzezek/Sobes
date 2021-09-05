from rest_framework import generics, status
from rest_framework.filters import SearchFilter
from rest_framework.permissions import IsAdminUser
from .permissions import IsStartDateBegin
from .serializers import (
    CategoryModelSerializer,
    QuestionModelSerializer,
    QuestionCreateModelSerializer,
    ChoiceModelSerializer,
    ChoiceCreateSerializer,
    AnswerNumberModelSerializer,
    AnswerModelSerializer,
)
from ..models import (
    Category,
    Question,
    Choice,
    Answer,
    AnswerNumber
)


class CategoryList(generics.ListAPIView):
    serializer_class = CategoryModelSerializer
    queryset = Category.objects.all()


class CategoryCreate(generics.CreateAPIView):
    serializer_class = CategoryModelSerializer
    queryset = Category.objects.all()
    permission_classes = (IsAdminUser,)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class CategoryUpdate(generics.RetrieveUpdateAPIView):
    serializer_class = CategoryModelSerializer
    queryset = Category.objects.all()
    permission_classes = (IsAdminUser, IsStartDateBegin)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class CategoryDestroy(generics.DestroyAPIView):
    serializer_class = CategoryModelSerializer
    queryset = Category.objects.all()
    permission_classes = (IsAdminUser, IsStartDateBegin)
    lookup_url_kwarg = 'pk'


class QuestionList(generics.ListAPIView):
    serializer_class = QuestionModelSerializer

    def get_queryset(self):
        queryset = Question.objects.filter(
            category=Category.objects.get(pk=self.kwargs['pk']))
        return queryset


class QuestionCreate(generics.ListCreateAPIView):
    serializer_class = QuestionCreateModelSerializer
    permission_classes = (IsAdminUser, IsStartDateBegin)

    def perform_create(self, serializer):
        serializer.save(category=Category.objects.get(pk=self.kwargs['pk']))

    def get_queryset(self):
        return Question.objects.filter(category=Category.objects.get(pk=self.kwargs['pk']))


class QuestionUpdate(generics.RetrieveUpdateAPIView):
    serializer_class = QuestionCreateModelSerializer
    queryset = Question.objects.all()
    permission_classes = (IsAdminUser, IsStartDateBegin)
    lookup_url_kwarg = 'q_pk'


class QuestionDestroy(generics.ListAPIView, generics.DestroyAPIView):
    serializer_class = QuestionModelSerializer
    permission_classes = (IsAdminUser, IsStartDateBegin)

    def get_queryset(self):
        return Question.objects.filter(pk=self.kwargs['q_pk'])


class ChoiceList(generics.ListAPIView):
    serializer_class = ChoiceModelSerializer
    permission_classes = (IsAdminUser, IsStartDateBegin)

    def get_queryset(self):
        return Question.objects.filter(pk=self.kwargs['q_pk'])


class ChoiceCreate(generics.CreateAPIView):
    serializer_class = ChoiceCreateSerializer
    permission_classes = (IsAdminUser, IsStartDateBegin)

    def perform_create(self, serializer):
        serializer.save(question=Question.objects.get(pk=self.kwargs['q_pk']))

    def get_queryset(self):
        return Choice.objects.filter(pk=self.kwargs['c_pk'])


class ChoiceDestroy(generics.ListAPIView, generics.DestroyAPIView):
    serializer_class = ChoiceModelSerializer
    permission_classes = (IsAdminUser, IsStartDateBegin)

    def get_queryset(self):
        return Choice.objects.filter(pk=self.kwargs['c_pk'])


class AnswerNumberCreate(generics.ListCreateAPIView):

    queryset = AnswerNumber.objects.all()
    serializer_class = AnswerNumberModelSerializer

    def perform_create(self, serializer):
        serializer.save(number=AnswerNumber.objects.latest('pk').pk + 1)


class AnswerCreate(generics.CreateAPIView):
    # queryset = Answer.objects.all()
    serializer_class = AnswerModelSerializer

    def perform_create(self, serializer):
        serializer.save(
            category=Category.objects.get(pk=self.kwargs['pk']),
            answer_numbers=AnswerNumber.objects.get(pk=self.kwargs['an_pk']),
            question=Question.objects.get(pk=self.kwargs['q_pk']),
        )


class AnswerSearch(generics.ListAPIView):
    serializer_class = AnswerModelSerializer
    filter_backends = [SearchFilter]
    search_fields = ['id',]

    def get_queryset(self):
        query = self.request.GET.get('search')
        object_list = Answer.objects.filter(pk=query)
        return object_list

