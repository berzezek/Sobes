from datetime import date

from django.forms import formset_factory
from django.http import HttpResponseRedirect, request
from django.db.models import Q
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse, reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, DeleteView, UpdateView

from .models import Category, Question, Choice, Answer
from .forms import CategoryForm, QuestionForm, ChoiceForm, AnswerForm, ChoiceFormSet
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
        context['categories'] = Category.objects.all()
        context['enable_interview'] = Category.objects.all().exclude(end_date__lte=date.today()).exclude(
            start_date__gte=date.today())  # Доступны в данный период времени
        context['count'] = context['enable_interview'].count()
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


class CategoryCreateView(LoginRequiredMixin, CreateView):
    model = Category
    template_name = 'interview/category/category_create.html'
    form_class = CategoryForm
    success_url = reverse_lazy('list')

    def form_valid(self, form):
        messages.success(self.request, f'Опрос - создан')
        form.instance.owner = self.request.user
        super().form_valid(form)
        return HttpResponseRedirect(self.get_success_url())


class CategoryUpdateView(LoginRequiredMixin, UpdateView):
    model = Category
    template_name = 'interview/category/category_edit.html'
    form_class = CategoryForm

    def form_valid(self, form):
        if Category.elapse_date:
            messages.error(self.request, f'Опрос начался!')
        else:
            messages.success(self.request, f'Опрос - обновлен')
            super().form_valid(form)
        return HttpResponseRedirect(self.get_success_url())


class CategoryDeleteView(LoginRequiredMixin, DeleteView):
    model = Category
    template_name = 'interview/category/category_delete.html'
    success_url = reverse_lazy('list')

    def form_valid(self, form):
        if Category.elapse_date:
            messages.error(self.request, f'Опрос начался!')
        else:
            messages.success(self.request, f'Опрос - удален')
            super().form_valid(form)
        return HttpResponseRedirect(self.get_success_url())


"""Вопросы"""


class QuestionListView(ListView):
    """Все Опросы"""
    model = Question
    template_name = 'interview/question/question_list.html'

    def get_context_data(self, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        category = Category.objects.filter(pk=self.kwargs['pk']).first()
        context['questions'] = Question.objects.filter(category=category).values()
        print(context['questions'].query)
        return context


class QuestionDetailView(DetailView):
    """Вопросы по категориям"""
    model = Category
    template_name = 'interview/question/question_detail.html'

    def get_context_data(self, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['category'] = Category.objects.filter(pk=self.kwargs['pk']).first()
        context['questions'] = Question.objects.filter(category=context['category']).filter(pk=self.kwargs['q_pk'])
        question = list(context['questions'].values())
        context['question'] = question[0]
        context['choice'] = Choice.objects.filter(question=context['questions'].first())
        return context


class QuestionCreateView(LoginRequiredMixin, CreateView):
    model = Question
    template_name = 'interview/question/question_create.html'
    form_class = QuestionForm

    def get_context_data(self, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['category'] = Category.objects.filter(pk=self.kwargs['pk']).first()
        return context

    def get_success_url(self):
        if Category.elapse_date:
            return reverse('list')
        return reverse('q_create', kwargs={'pk': self.kwargs['pk']})

    def form_valid(self, form):
        if not Category.elapse_date:
            messages.error(self.request, f'Опрос начался!')
        else:
            messages.success(self.request, f'Вопрос - добавлен')
            form.instance.category = Category.objects.filter(pk=self.kwargs['pk']).first()
            super().form_valid(form)
        return HttpResponseRedirect(self.get_success_url())


class QuestionUpdateView(LoginRequiredMixin, UpdateView):
    model = Question
    template_name = 'interview/question/question_edit.html'
    form_class = QuestionForm
    pk_url_kwarg = 'q_pk'

    def get_context_data(self, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['category'] = Category.objects.filter(pk=self.kwargs['pk']).first()
        context['questions'] = Question.objects.filter(category=context['category']).filter(pk=self.kwargs['q_pk'])
        return context

    def form_valid(self, form):
        if not Category.elapse_date:
            messages.error(self.request, f'Опрос начался!')
        else:
            messages.success(self.request, f'Вопрос - обновлен')
            form.instance.category = Category.objects.filter(pk=self.kwargs['pk']).first()
            super().form_valid(form)
        return HttpResponseRedirect(self.get_success_url())

    def get_success_url(self):  # Переадресация по "question.type"
        if not Category.elapse_date:
            return reverse('list')
        if Question.objects.filter(category=Category.objects.filter(pk=self.kwargs['pk']).first()).filter(
                pk=self.kwargs['q_pk']).exclude(type='1'):
            return reverse('choice_create', kwargs={'pk': self.kwargs['pk'], 'q_pk': self.kwargs['q_pk']})
        else:
            return reverse('q_create', kwargs={'pk': self.kwargs['pk']})


class QuestionDeleteView(LoginRequiredMixin, DeleteView):
    model = Question
    template_name = 'interview/question/question_delete.html'
    pk_url_kwarg = 'q_pk'

    def get_context_data(self, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['category'] = Category.objects.filter(pk=self.kwargs['pk']).first()
        context['question'] = Question.objects.filter(category=context['category']).filter(
            pk=self.kwargs['q_pk']).first()
        return context

    def get_success_url(self):
        if not Category.elapse_date:
            return reverse('list')
        return reverse('category_detail', kwargs={'pk': self.kwargs['pk']})

    def form_valid(self, form):
        if not Category.elapse_date:
            messages.error(self.request, f'Опрос начался!')
        else:
            messages.success(self.request, f'Вопрос - удален')
            super().form_valid(form)
        return HttpResponseRedirect(self.get_success_url())


"""Добавить вариант"""


class ChoiceCreateView(LoginRequiredMixin, CreateView):
    """Добавление варианта ответа"""
    model = Choice
    template_name = 'interview/choice/choice_create.html'
    # form_class = formset_factory(ChoiceForm(instance=), extra=3)
    form_class = ChoiceForm

    def get_context_data(self, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['category'] = Category.objects.filter(pk=self.kwargs['pk']).first()
        context['question'] = Question.objects.filter(pk=self.kwargs['q_pk']).first()
        return context

    def get_success_url(self):
        if not Category.elapse_date:
            return reverse('list')
        return reverse('choice_create', kwargs={'pk': self.kwargs['pk'], 'q_pk': self.kwargs['q_pk']})

    def form_valid(self, form):
        if not Category.elapse_date:
            messages.error(self.request, f'Опрос начался!')
        else:
            form.instance.question = Question.objects.filter(pk=self.kwargs['q_pk']).first()
            messages.success(self.request, f'Вариант ответа - добавлен')
            super().form_valid(form)
        return HttpResponseRedirect(self.get_success_url())


class ChoiceDeleteView(LoginRequiredMixin, DeleteView):
    model = Choice
    template_name = 'interview/choice/choice_delete.html'
    pk_url_kwarg = 'c_pk'

    def get_context_data(self, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['category'] = Category.objects.filter(pk=self.kwargs['pk']).first()
        context['question'] = Question.objects.filter(category=context['category']).filter(
            pk=self.kwargs['q_pk']).first()
        context['choice'] = Choice.objects.filter(question=context['question']).filter(pk=self.kwargs['c_pk']).first()
        return context

    def get_success_url(self):
        return reverse('q_detail', kwargs={'pk': self.kwargs['pk'], 'q_pk': self.kwargs['q_pk']})

    def form_valid(self, form):
        if not Category.elapse_date:
            messages.error(self.request, f'Опрос начался!')
        else:
            messages.success(self.request, f'Вопрос - удален')
            super().form_valid(form)
        return HttpResponseRedirect(self.get_success_url())


"""Ответы пользователей"""


class AnswerListView(ListView):
    """Поиск ответов пользователей по id"""
    model = Answer
    template_name = 'interview/answer/answer_search.html'

    def get_queryset(self):
        query = self.request.GET.get('q')
        object_list = Answer.objects.filter(id=query)
        return object_list


class AnswerCreateView(CreateView):
    model = Answer
    form_class = AnswerForm
    template_name = 'interview/answer/answer_create.html'

    success_url = reverse_lazy('list')

    def form_valid(self, form):
        messages.success(self.request, f'Опрос - пройден')
        form.instance.owner = self.request.user
        form.instance.category = Category.objects.filter(pk=self.kwargs['pk']).first()
        form.instance.question = Question.objects.filter(category=form.instance.category).first()
        # form.instance.answer_choice = Choice.objects.filter(question=form.instance.question).first()
        # form.instance.answer_multi = Choice.objects.filter(question=form.instance.question).first()
        super().form_valid(form)
        return HttpResponseRedirect(self.get_success_url())

    def get_context_data(self, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['category'] = Category.objects.filter(pk=self.kwargs['pk']).first()
        context['questions'] = Question.objects.filter(category=context['category'])
        return context

    # def get_success_url(self):
    #     return reverse('choice_create', kwargs={'pk': self.kwargs['pk'], 'q_pk': self.kwargs['q_pk']})
