from datetime import date

from django.http import HttpResponseRedirect, request
from django.db.models import Q
from django.shortcuts import render, get_object_or_404
from django.urls import reverse, reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, DeleteView, UpdateView

from .models import Category, Question, Choice, Answer
from .forms import CategoryForm, QuestionForm, ChoiceForm, AnswerForm
from django.contrib import messages

from django.contrib.auth.mixins import LoginRequiredMixin

"""Опросы"""


class CategoryListView(ListView):
    """Все Опросы"""
    model = Category
    template_name = 'interview/category/category_list.html'
    ordering = ['-id']

    def get_context_data(self, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all().exclude(end_date__lte=date.today()).order_by('-end_date')
        context['count'] = context['categories'].count()
        context['title'] = 'Главная'
        return context


class CategoryDetailView(DetailView):
    """Опрос отдельно"""
    model = Category
    template_name = 'interview/category/category_detail.html'

    def get_context_data(self, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = Category.objects.filter(pk=self.kwargs['pk']).first()
        context['questions'] = Question.objects.filter(category=context['title'])
        context['count'] = context['questions'].count()
        return context


class CategoryCreateView(CreateView, LoginRequiredMixin):
    model = Category
    template_name = 'interview/category/category_create.html'
    form_class = CategoryForm
    success_url = reverse_lazy('list')

    def form_valid(self, form):
        messages.success(self.request, f'Опрос - создан')
        form.instance.owner = self.request.user
        super().form_valid(form)
        return HttpResponseRedirect(self.get_success_url())


class CategoryUpdateView(UpdateView):
    model = Category
    template_name = 'interview/category/category_edit.html'
    form_class = CategoryForm

    def form_valid(self, form):
        messages.success(self.request, f'Опрос - обновлен')
        super().form_valid(form)
        return HttpResponseRedirect(self.get_success_url())


class CategoryDeleteView(DeleteView):
    model = Category
    template_name = 'interview/category/category_delete.html'
    success_url = reverse_lazy('list')

    def form_valid(self, form):
        messages.success(self.request, f'Опрос - удален')
        super().form_valid(form)
        return HttpResponseRedirect(self.get_success_url())


"""Вопросы"""


class QuestionDetailView(DetailView):
    """Вопросы по категориям"""
    model = Category
    template_name = 'interview/question/question_detail.html'

    def get_context_data(self, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        category = Category.objects.filter(pk=self.kwargs['pk']).first()
        context['questions'] = Question.objects.filter(category=category).filter(pk=self.kwargs['q_pk'])
        question = list(Question.objects.filter(category=category).filter(pk=self.kwargs['q_pk']).values())
        context['question'] = question[0]
        context['choice'] = Choice.objects.filter(question=Question.objects.filter(category=category).filter(pk=self.kwargs['q_pk']).first())
        return context


class QuestionCreateView(CreateView):
    model = Question
    template_name = 'interview/question/question_create.html'
    form_class = QuestionForm
    success_url = reverse_lazy('list')

    def get_context_data(self, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['category'] = Category.objects.filter(pk=self.kwargs['pk']).first()
        return context

    def form_valid(self, form):
        messages.success(self.request, f'Вопрос - добавлен')
        super().form_valid(form)
        return HttpResponseRedirect(self.get_success_url())


class QuestionUpdateView(UpdateView):
    model = Question
    template_name = 'interview/question/question_edit.html'
    form_class = QuestionForm

    def get_context_data(self, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['category'] = Category.objects.filter(pk=self.kwargs['pk']).first()
        # context['questions'] = Question.objects.filter(category=context['category']).filter(pk=self.kwargs['q_pk'])
        return context

    def form_valid(self, form):
        messages.success(self.request, f'Вопрос - обновлен')
        super().form_valid(form)
        return HttpResponseRedirect(self.get_success_url())


class QuestionDeleteView(DeleteView):
    model = Question
    template_name = 'interview/question/question_delete.html'
    success_url = reverse_lazy('list')

    def get_context_data(self, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['category'] = Category.objects.filter(pk=self.kwargs['pk']).first()
        context['question'] = Question.objects.filter(pk=self.kwargs['q_pk']).first()
        return context

    def form_valid(self, form):
        messages.success(self.request, f'Вопрос - удален')
        # super().form_valid(form)
        return HttpResponseRedirect(self.get_success_url())


"""Добавить вариант"""


class ChoiceCreateView(CreateView):
    """Добавление варианта ответа"""
    model = Choice
    template_name = 'interview/choice/choice_create.html'
    form_class = ChoiceForm
    success_url = 'list'

    def get_context_data(self, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['category'] = Category.objects.filter(pk=self.kwargs['pk']).first()
        context['question'] = Question.objects.filter(pk=self.kwargs['q_pk']).first()
        return context

    def form_valid(self, form):
        form.instance.question = Question.objects.filter(pk=self.kwargs['q_pk']).first()
        messages.success(self.request, f'Вариант ответа - добавлен')
        super().form_valid(form)
        return HttpResponseRedirect(self.get_success_url())


"""Ответы пользователей"""


class AnswerListView(ListView):
    """Ответы пользователей"""
    model = Answer
    template_name = 'interview/answer/answer_search.html'

    def get_queryset(self):
        query = self.request.GET.get('q')
        object_list = Answer.objects.filter(
            Q(pk__icontains=query)
        )
        return object_list


# class AnswerCreateView(CreateView):
#     model = Answer
#     form_class = AnswerForm
#     template_name = 'interview/answer/answer_create.html'
#     success_url = reverse_lazy('list')
#
#     def form_valid(self, form):
#         messages.success(self.request, f'Опрос - пройден')
#         super().form_valid(form)
#         return HttpResponseRedirect(self.get_success_url())


def get_name(request):
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = AnswerForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required
            # ...
            # redirect to a new URL:
            return HttpResponseRedirect('list')

    # if a GET (or any other method) we'll create a blank form
    else:
        form = AnswerForm()

    return render(request, 'interview/answer/answer_create.html', {'form': form})