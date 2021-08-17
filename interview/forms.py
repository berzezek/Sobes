from datetime import date

from django import forms
from .models import Category, Question, Choice, Answer
from django.contrib.auth.models import User


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
        initial=date.replace(date.today(), month=(date.today().month + 1)),
        label='Начало опроса',
        required=False,
        widget=forms.SelectDateWidget(
            attrs={'class': 'form-control w-auto my-1 ', 'placeholder': 'После начала опроса вы не сможете изменить его'}
            )
    )

    end_date = forms.DateField(
        initial=date.replace(date.today(), year=(date.today().year + 1)),
        label='Окончание опроса',
        required=False,
        widget=forms.SelectDateWidget(
            attrs={'class': 'form-control w-auto d-flex justify-content-between'}
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
        fields = [
            # 'question',
            'title'
        ]

    # question = forms.ModelChoiceField(
    #     queryset=Question.objects.all(),
    #     label='Наименование вопроса',
    #     required=False,
    #     widget=forms.Select(
    #         attrs={'class': 'form-control mb-3'}
    #     ),
    # )
    title = forms.CharField(
        label='Вариант',
        required=False,
        widget=forms.TextInput(
            attrs={'class': 'form-control mb-3'}
        )
    )



class AnswerForm(forms.ModelForm):

    class Meta:
        model = Answer
        fields = [
            # 'owner',
            # 'category',
            'question',
            'answer_text',
            'answer_choice',
            'answer_multi'
        ]
    #
    # question = forms.CharField(
    #     label='Вопрос',
    #     required=True,
    #     widget=forms.TextInput(
    #         attrs={'class': 'form-control mb-3'}
    #     )
    # )