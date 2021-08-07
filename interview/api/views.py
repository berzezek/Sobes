from datetime import date

from django.db.models import Q
from django.http import Http404

from main.interview.models import Category, Question, Choice, Answer
from .permissions import IsStartDateBegin
from .serializers import QuestionModelSerializer, CategoryModelSerializer, ChoiceModelSerializer, AnswerModelSerializer
from rest_framework.response import Response
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404, redirect
from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework import permissions, generics, status


class CategoryCreate(generics.ListCreateAPIView):
    serializer_class = CategoryModelSerializer
    queryset = Category.objects.all()
    # renderer_classes = [TemplateHTMLRenderer]
    # template_name = 'interview/category_list.html'
    #
    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class CategoryList(generics.ListAPIView):
    serializer_class = CategoryModelSerializer
    # queryset = Category.objects.all()
    # renderer_classes = [TemplateHTMLRenderer]
    # template_name = 'interview/category_list.html'
    # permission_classes = [IsStartDateBegin]

    def get_queryset(self, *args, **kwargs):
        queryset_list = Category.objects.all()
        query = self.request.GET.get('q')
        if query:
            queryset_list = queryset_list.filter(
                Q(id__icontains=query)|
                Q(start_date__gte=query)
            ).distinct()
        return queryset_list

    # def get(self, request):
    #     category = Category.objects.all().exclude(end_date__lte=date.today())
    #     count = category.count()
    #     serializer = CategoryModelSerializer(Category.objects.all(), many=True)
    #     return Response({'serializer': serializer.data, 'category': category, 'count': count})


class CategoryDetail(generics.RetrieveUpdateAPIView):
    serializer_class = CategoryModelSerializer
    queryset = Category.objects.all()
    permission_classes = [IsStartDateBegin]
    # renderer_classes = [TemplateHTMLRenderer]
    # template_name = 'interview/category_detail.html'
    #
    # def get(self, request, pk):
    #     category = get_object_or_404(Category, pk=pk)
    #     serializer = CategoryModelSerializer(category)
    #     return Response({'serializer': serializer, 'category': category})
    #
    # def post(self, request, pk):
    #     category = get_object_or_404(Category, pk=pk)
    #     serializer = CategoryModelSerializer(category, data=request.data)
    #     if not serializer.is_valid():
    #         return Response({'serializer': serializer, 'category': category})
    #     serializer.save()
    #     return redirect('category_detail', pk=pk)
    #
    # def perform_create(self, serializer):
    #     serializer.save(owner=self.request.user)


class CategoryDestroy(generics.DestroyAPIView):
    serializer_class = CategoryModelSerializer
    queryset = Category.objects.all()
    # renderer_classes = [TemplateHTMLRenderer]
    # template_name = 'interview/category_delete.html'
    # permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    #
    # def get(self, request, pk):
    #     category = get_object_or_404(Category, pk=pk)
    #     serializer = CategoryModelSerializer(category)
    #     return Response({'serializer': serializer, 'category': category})

    # def delete(self, request, pk):
    #     category = get_object_or_404(Category, pk=pk)
    #     category.delete()
    #     return Response(status=status.HTTP_204_NO_CONTENT)
    permission_classes = [IsStartDateBegin, permissions.IsAuthenticated]

# class QuestionList(generics.ListCreateAPIView):
#     permission_classes = [permissions.IsAuthenticatedOrReadOnly]
#     serializer_class = QuestionModelSerializer
#     queryset = Question.objects.all()
#
#
# class ChoiceList(generics.ListCreateAPIView):
#
#     queryset = Choice.objects.all()
#     serializer_class = ChoiceModelSerializer
#
#
# class AnswerList(generics.ListCreateAPIView):
#
#     queryset = Answer.objects.all()
#     serializer_class = AnswerModelSerializer
