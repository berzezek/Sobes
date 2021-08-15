from datetime import date

from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse, reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, DeleteView, UpdateView

from .models import Category, Question, Choice, Answer, Poll
from .forms import CategoryForm, QuestionForm, ChoiceForm, AnswerForm, PollForm
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
        context['categories'] = Category.objects.all().exclude(end_date__lte=date.today())
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
    model = Question
    template_name = 'interview/question/question_detail.html'

    def get_context_data(self, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        # category = Category.objects.filter(pk=self.kwargs['pk']).first()
        # questions = Question.objects.filter(category=category).filter(pk=self.kwargs['q_pk'])
        # context['category'] = category
        context['questions'] = Question.objects.filter(pk=self.kwargs['pk'])
        # context['choice'] = Choice.objects.filter(question=questions.first())
        return context


class QuestionCreateView(CreateView):
    model = Question
    template_name = 'interview/question/question_create.html'
    form_class = QuestionForm

    def form_valid(self, form):
        messages.success(self.request, f'Вопрос - добавлен')
        super().form_valid(form)
        return HttpResponseRedirect(self.get_success_url())


class QuestionUpdateView(UpdateView):
    model = Question
    template_name = 'interview/question/question_edit.html'
    form_class = QuestionForm
    success_url = reverse_lazy('list')

    def get_context_data(self, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        # questions = Question.objects.filter(category=category).filter(pk=self.kwargs['q_pk'])
        context['category'] = Category.objects.filter(pk=self.kwargs['pk']).first()
        # context['questions'] = Question.objects.filter(pk=self.kwargs['q_pk'])
        # context['choice'] = Choice.objects.filter(question=questions.first())
        return context

    def form_valid(self, form):
        messages.success(self.request, f'Вопрос - обновлен')
        super().form_valid(form)
        return HttpResponseRedirect(self.get_success_url())


class QuestionDeleteView(DeleteView):
    model = Question
    template_name = 'interview/question/question_delete.html'
    success_url = '/'

    def get_context_data(self, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        # context['category'] = Category.objects.filter(pk=self.kwargs['pk']).first()
        return context

    def form_valid(self, form):
        messages.success(self.request, f'Вопрос - удален')
        super().form_valid(form)
        return HttpResponseRedirect(self.get_success_url())


"""Добавить вариант"""


class ChoiceCreateView(CreateView):
    """Добавление варианта ответа"""
    model = Choice
    template_name = 'interview/choice/choice_create.html'
    form_class = ChoiceForm

    def get_context_data(self, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        category = Category.objects.filter(pk=self.kwargs['pk']).first()
        questions = Question.objects.filter(category=category).filter(pk=self.kwargs['q_pk'])
        context['category'] = Category.objects.filter(pk=self.kwargs['pk'])
        context['questions'] = Question.objects.filter(pk=self.kwargs['q_pk'])
        context['choice'] = Choice.objects.filter(question=questions.first())
        return context


"""Ответы пользователей"""


class AnswerListView(ListView):
    """Ответы пользователей"""
    model = Answer
    context_object_name = 'answers'
    template_name = 'interview/answer/answer_list.html'


class AnswerCreateView(CreateView):
    model = Answer
    form_class = AnswerForm
    template_name = 'interview/answer/answer_create.html'


class PollCreateView(CreateView):
    model = Poll
    template_name = 'interview/poll/poll_create.html'
    fields = ['user', 'answer']

    def get_success_url(self):
        # return reverse('poll', kwargs={'pk': self.object.pk})
        return reverse('list')


def poll_create(request):
    answer = Answer.objects.all()
    if request.method == 'POST':
        form = PollForm(request.POST)
        if form.is_valid():
            form.save()
            for el in answer:
                mess = el.pk
            messages.success(request, f'Вы ответили на опрос. Ответы досупны по ID {mess}')
            return redirect('list')
    else:
        form = AnswerForm()
    context = {'form': form, 'title': 'Создать опрос'}
    return render(request, 'interview/answer/answer_create.html', context)
