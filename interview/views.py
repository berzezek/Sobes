from datetime import date

from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect
from django.urls import reverse, reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, DeleteView, UpdateView

from .forms import CategoryForm, QuestionForm, AnswerForm, ChoiceFormSet, AnswerNumberForm
from .models import Category, Question, Choice, Answer, AnswerNumber

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

    def get_success_url(self):
        return reverse('q_create', kwargs={'pk': Category.objects.latest('pk').pk})

    def form_valid(self, form):
        form.instance.owner = self.request.user
        super().form_valid(form)
        messages.success(self.request, f'Опрос "{Category.objects.latest("pk")}"- создан')
        messages.success(self.request, f'Приступайте к добавлению вопросов')
        return HttpResponseRedirect(self.get_success_url())


class CategoryUpdateView(LoginRequiredMixin, UpdateView):
    model = Category
    template_name = 'interview/category/category_edit.html'
    form_class = CategoryForm

    def form_valid(self, form):
        c = Category.objects.filter(pk=self.kwargs["pk"]).first()
        if Category.elapse == True:
            messages.error(self.request, f'Опрос "{c}" начался!')
        else:
            messages.success(self.request, f'Опрос "{c}" - обновлен')
            super().form_valid(form)
        return HttpResponseRedirect(self.get_success_url())


class CategoryDeleteView(LoginRequiredMixin, DeleteView):
    model = Category
    template_name = 'interview/category/category_delete.html'
    success_url = reverse_lazy('list')

    def form_valid(self, form):
        if Category.elapse == True:
            messages.error(self.request, f'Опрос "{Category.objects.filter(pk=self.kwargs["pk"]).first()}" начался!')
        else:
            messages.error(self.request, f'Опрос "{Category.objects.filter(pk=self.kwargs["pk"]).first()}" - удален')
            super().form_valid(form)
        return HttpResponseRedirect(self.get_success_url())


"""Вопросы"""


# class QuestionListView(ListView):
#     """Все Опросы"""
#     model = Question
#     template_name = 'interview/question/question_list.html'
#
#     def get_context_data(self, object_list=None, **kwargs):
#         context = super().get_context_data(**kwargs)
#         category = Category.objects.filter(pk=self.kwargs['pk']).first()
#         context['questions'] = Question.objects.filter(category=category).values()
#         print(context['questions'].query)
#         return context


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
        if Category.elapse == True:
            return reverse('list')
        else:
            if Question.objects.latest('id').type == '1':
                return reverse('q_create', kwargs={'pk': self.kwargs['pk']})
            else:
                return reverse('choice_create',
                               kwargs={'pk': self.kwargs['pk'], 'q_pk': Question.objects.latest('pk').pk})

    def form_valid(self, form):
        # if Category.elapse:
        if Category.elapse == True:
            messages.error(self.request, f'Опрос "{Category.objects.filter(pk=self.kwargs["pk"]).first()}" начался!')
        else:
            form.instance.category = Category.objects.filter(pk=self.kwargs['pk']).first()
            super().form_valid(form)
            messages.success(self.request, f'Вопрос "{Question.objects.latest("pk")}"- добавлен')
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
        c = Category.objects.filter(pk=self.kwargs["pk"]).first()
        q = Question.objects.filter(pk=self.kwargs["q_pk"]).first()
        if Category.elapse == True:
            messages.error(self.request, f'Опрос "{c}" начался!')
        else:
            messages.success(self.request, f'Вопрос {q}- обновлен')
            form.instance.category = c
            super().form_valid(form)
            messages.success(self.request,
                             f'и теперь вопрос звучит так: "{q}", с вариантом ответа: {q.get_type_display()}')
        return HttpResponseRedirect(self.get_success_url())

    def get_success_url(self):  # Переадресация по "question.type"
        if Category.elapse == True:
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
        if Category.elapse == True:
            return reverse('list')
        else:
            return reverse('category_detail', kwargs={'pk': self.kwargs['pk']})

    def form_valid(self, form):
        if Category.elapse == True:
            messages.error(self.request, f'Опрос "{Category.objects.filter(pk=self.kwargs["pk"]).first()}" начался!')
        else:
            messages.error(self.request, f'Вопрос - удален')
            super().form_valid(form)
        return HttpResponseRedirect(self.get_success_url())


"""Добавить вариант"""


class ChoiceCreateView(LoginRequiredMixin, CreateView):
    """Добавление варианта ответа"""
    model = Choice
    template_name = 'interview/choice/choice_create.html'
    fields = ['title']

    def get_context_data(self, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['formset'] = ChoiceFormSet()
        context['category'] = Category.objects.filter(pk=self.kwargs['pk']).first()
        context['question'] = Question.objects.filter(pk=self.kwargs['q_pk']).first()
        return context

    def get_success_url(self):
        if Question.objects.get(pk=self.kwargs['q_pk']).type == '1':
            return reverse('q_create', kwargs={'pk': self.kwargs['pk']})
        return reverse('choice_create', kwargs={'pk': self.kwargs['pk'], 'q_pk': self.kwargs['q_pk']})

    def form_valid(self, formset):
        if Category.elapse == True:
            messages.error(self.request, f'Опрос "{Category.objects.filter(pk=self.kwargs["pk"]).first()}" начался!')
        else:
            formset.instance.title = self.request.POST['form-0-title']
            formset.instance.question = Question.objects.filter(pk=self.kwargs['q_pk']).first()
            super().form_valid(formset)
            messages.success(self.request, f'Вариант ответа "{Choice.objects.order_by("-pk").first()}" - добавлен')
        return HttpResponseRedirect(self.get_success_url())


class ChoiceDeleteView(LoginRequiredMixin, DeleteView):
    """Удаление варианта ответа"""
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
        if Category.elapse == True:
            messages.error(self.request, f'Опрос "{Category.objects.filter(pk=self.kwargs["pk"]).first()}" начался!')
        else:
            messages.success(self.request, f'Вопрос - удален')
            super().form_valid(form)
        return HttpResponseRedirect(self.get_success_url())


"""База ответов"""


class AnswerNumberCreateView(CreateView):
    """Создание номера для опроса пользователя"""
    model = AnswerNumber
    form_class = AnswerNumberForm
    template_name = 'interview/answer/answer_number_create.html'

    def get_success_url(self):
        return reverse('answer_create',
                       kwargs={
                           'pk': self.kwargs['pk'],
                           'q_pk': Question.objects.filter(category=Category.objects.get(pk=self.kwargs['pk'])).first().pk,
                           'an_pk': AnswerNumber.objects.latest('number').pk
                       })

    def form_valid(self, form):
        try:
            a = int(str(AnswerNumber.objects.latest('pk')))
        except AnswerNumber.DoesNotExist:
            a = 0
        form.instance.number = a
        super().form_valid(form)
        messages.success(self.request, f'Опрос {a + 1} начался')
        return HttpResponseRedirect(self.get_success_url())

    def get_context_data(self, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['category'] = Category.objects.filter(pk=self.kwargs['pk']).first()
        context['questions'] = Question.objects.filter(category=self.kwargs['pk'])
        return context


class AnswerNumberListView(ListView):
    """Поиск ответов пользователей по id"""
    model = Answer
    template_name = 'interview/answer/answer_number_list.html'

    def get_queryset(self):
        query = self.request.GET.get('q')
        object_list = Answer.objects.filter(answer_numbers=query)
        return object_list

    def get_context_data(self, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['answer'] = self.request.GET
        context['category'] = Answer.objects.all()
        return context


"""Ответы пользователей"""


class AnswerCreateView(CreateView):
    model = Answer
    form_class = AnswerForm
    template_name = 'interview/answer/answer_create.html'

    def get_success_url(self):
        question = Question.objects.filter(category=Category.objects.get(pk=self.kwargs['pk']))
        print(question.count())
        try:
            return reverse('answer_create', kwargs={
                'pk': self.kwargs['pk'],
                'q_pk': Question.objects.filter(category=Category.objects.filter(pk=self.kwargs['pk']).first()).first().pk + 1,
                'an_pk': self.kwargs['an_pk']
            })
        except Question.DoesNotExist:
            return reverse('list',
                           messages.success(self.request, f'Опрос {Category.objects.get(pk=self.kwargs["pk"])} пройден,'
                                                          f'№ {Answer.objects.get(pk=self.kwargs["an_pk"]).answer_numbers}'))

    def form_valid(self, form):
        form.instance.answer_numbers = AnswerNumber.objects.latest('number')
        form.instance.category = Category.objects.get(pk=self.kwargs['pk'])
        form.instance.question = Question.objects.get(pk=self.kwargs['q_pk'])
        super().form_valid(form)
        messages.success(self.request, f'Ответ на вопрос {form.instance.question} - получен')
        return HttpResponseRedirect(self.get_success_url())

    def get_context_data(self, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['category'] = Category.objects.get(pk=self.kwargs['pk'])
        context['question'] = Question.objects.get(pk=self.kwargs['q_pk'])
        return context

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['choice'] = Choice.objects.filter(question=Question.objects.get(pk=self.kwargs['q_pk']))
        return kwargs
