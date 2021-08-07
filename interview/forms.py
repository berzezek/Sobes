from django import forms
from .models import Category
from django.contrib.auth.models import User


class CategoryForm(forms.ModelForm):
    owner = forms.ModelChoiceField(
        queryset=User.objects.all(),
        label='Автор',
        required=True,
        widget=forms.Select(
            attrs={'class': 'form-select'}
        ),

    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['owner'].queryset = User.objects.filter(id=1)

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
        widget=forms.Textarea(
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

    class Meta:
        model = Category
        fields = ['owner', 'title', 'description', 'start_date', 'end_date']