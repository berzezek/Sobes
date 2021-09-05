from datetime import date

from django import forms
from django.forms import modelformset_factory, BaseModelFormSet

from .models import Category, Question, Choice, Answer, AnswerNumber


class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = [
            'title',
            'description',
            'start_date',
            'end_date'
        ]

    title = forms.CharField(
        label='Наименование опроса',
        required=True,
        widget=forms.TextInput(
            attrs={'class': 'form-control mb-3'}
        )
    )

    description = forms.CharField(
        label='Описание опроса',
        required=True,
        widget=forms.TextInput(
            attrs={'class': 'form-control mb-3'}
        )
    )

    start_date = forms.DateField(
        # initial=date.replace(date.today(), month=(date.today().month + 1)),
        label='Начало опроса',
        required=False,
        widget=forms.DateInput(
            attrs={'class': 'form-control-sm', 'type': 'date'}
        )
    )

    end_date = forms.DateField(
        # initial=date.replace(date.today(), year=(date.today().year + 1)),
        label='Окончание опроса',
        required=False,
        widget=forms.DateInput(
            attrs={'class': 'form-control-sm', 'type': 'date'}
        )
    )


class QuestionForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = [
            'title',
            'type',
        ]

    title = forms.CharField(
        label='Наименование вопроса',

        required=True,
        widget=forms.TextInput(
            attrs={'class': 'form-control mb-3'}
        )
    )

    TYPE_QUESTION = (
        ('1', 'Текст'),
        ('2', 'Выбор'),
        ('3', 'Опция'),
    )
    type = forms.ChoiceField(
        label='Тип ответа',
        choices=TYPE_QUESTION,
        required=False,
        widget=forms.Select(
            attrs={'class': 'form-control'}
        )
    )


class ChoiceForm(forms.ModelForm):
    class Meta:
        model = Choice
        # fields = '__all__'
        fields = ['title']

    # question = forms.ModelChoiceField(
    #
    #     queryset=Question.objects.all(),
    #     label='Вопрос',
    #     widget=forms.Select(
    #         attrs={'class': 'form-control mb-3'}
    #     )
    # )

    title = forms.CharField(
        label='Вариант',
        required=False,
        widget=forms.TextInput(
            attrs={'class': 'form-control mb-3'}
        )
    )


ChoiceFormSet = forms.formset_factory(
    ChoiceForm,
    # extra=3
)


class AnswerNumberForm(forms.ModelForm):
    class Meta:
        model = AnswerNumber
        # fields = ['number']
        fields = []


class AnswerForm(forms.ModelForm):
    class Meta:
        model = Answer
        fields = [
            # 'owner',
            # 'category',
            # 'question',
            'answer_text',
            'answer_choice',
            'answer_multi'
        ]

    answer_text = forms.CharField(
        label='Ответ текстом',
        required=False,
        widget=forms.Textarea(
            attrs={'class': 'form-control mb-3', 'rows': 3}
        )
    )

    answer_choice = forms.ModelChoiceField(
        queryset=Choice.objects.none(),
        label='Выбор',
        required=False,
        widget=forms.Select(
            attrs={'class': 'form-control mb-3'}
        )
    )

    answer_multi = forms.ModelMultipleChoiceField(
        queryset=Choice.objects.none(),
        label='Опция',
        required=False,
        widget=forms.SelectMultiple(
            attrs={'class': 'form-control mb-3'}
        )
    )

    def __init__(self, choice, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['answer_choice'].queryset = choice
        self.fields['answer_multi'].queryset = choice
