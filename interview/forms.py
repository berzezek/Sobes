from django import forms
from .models import Category, Question, Choice, Answer
from django.contrib.auth.models import User


class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = [
            'owner',
            'title',
            'description',
            'start_date',
            'end_date'
        ]

    owner = forms.ModelChoiceField(
        queryset=User.objects.all(),
        label='Автор',
        required=True,
        widget=forms.Select(
            attrs={'class': 'form-select'}
        ),
    )

    title = forms.CharField(
        label='Название опроса',
        required=True,
        widget=forms.TextInput(
            attrs={'class': 'form-control'}
        )
    )

    description = forms.CharField(
        label='Описание опроса',
        required=True,
        widget=forms.TextInput(
            attrs={'class': 'form-control'}
        )
    )

    start_date = forms.DateField(
        label='Начало опроса',
        required=False,
        widget=forms.SelectDateWidget(
            attrs={'class': 'form-control w-25 my-1', 'placeholder': 'После начала опроса вы не сможете изменить его'}
            )
    )

    end_date = forms.DateField(
        label='Окончание опроса',
        required=False,
        widget=forms.SelectDateWidget(
            attrs={'class': 'form-control w-25 my-1', 'placeholder': 'После начала опроса вы не сможете изменить его'}
        )
    )

class QuestionForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = [
            'category',
            'title',
            'type',
        ]

    category = forms.ModelChoiceField(
        queryset=Category.objects.all(),
        label='Наименование опроса',
        required=True,
        widget=forms.Select(
            attrs={'class': 'form-select'}
        ),
    )

    title = forms.CharField(
        label='Название вопроса',

        required=True,
        widget=forms.TextInput(
            attrs={'class': 'form-control'}
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
            'question',
            'answer',
        ]
    question = forms.ModelChoiceField(
        queryset=Question.objects.all(),
        label='Наименование вопроса',
        required=False,
        widget=forms.Select(
            attrs={'class': 'form-select'}
        ),
    )
    answer = forms.CharField(
        label='Вариант',
        required=False,
        widget=forms.TextInput(
            attrs={'class': 'form-control'}
        )
    )
