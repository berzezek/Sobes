from datetime import date

from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse


class Category(models.Model):
    """Категория опросов"""
    class Meta:
        verbose_name = 'Опрос'
        verbose_name_plural = 'Опросы'
        ordering = ['-start_date']
        permissions = [("elapse_date", "Опрос - начался!")]

    owner = models.ForeignKey(User, verbose_name='Автор', on_delete=models.CASCADE)
    title = models.CharField('Наименование опроса', max_length=150, unique=True)
    description = models.CharField('Описание опроса', max_length=255)
    start_date = models.DateField('Дата начала опроса', blank=True, null=True)
    end_date = models.DateField('Дата окончания опроса', blank=True, null=True)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('category_detail', kwargs={'pk': self.pk})

    def elapse(self):  # Используется во views
        if Category.objects.filter(pk=self.pk).filter(start_date__lte=date.today()):
            return True
        else:
            return False

    def elapse_date(self):  # Используется в шаблонах
        if self.start_date:
            if (self.start_date - date.today()).days < 0:
                return False
        return True


class Question(models.Model):
    """Вопросы"""

    class Meta:
        verbose_name = 'Вопрос'
        verbose_name_plural = 'Вопросы'

    TYPE_QUESTION = (
        ('1', 'Текст'),
        ('2', 'Выбор'),
        ('3', 'Опция'),
    )

    category = models.ForeignKey(Category, verbose_name='Наименование опроса', on_delete=models.CASCADE, blank=True,
                                 null=True, related_name='category')
    title = models.CharField('Вопрос', max_length=255)
    type = models.CharField('Тип ответа', max_length=1, choices=TYPE_QUESTION, default='1')

    def __str__(self):
        return str(self.title)

    def get_absolute_url(self):
        return reverse('q_detail', kwargs={'pk': self.category.pk, 'q_pk': self.pk})

    def get_delete_url(self):
        return reverse('q_delete', kwargs={'pk': self.category.pk, 'q_pk': self.pk})

    def get_create_url(self):
        return reverse('q_create', kwargs={'pk': self.category.pk})


class Choice(models.Model):
    """Промежуточная модель для формирования вариантов ответов"""

    class Meta:
        verbose_name = 'Вариант ответа'
        verbose_name_plural = 'Варианты ответов'

    title = models.CharField('Вариант ответа', max_length=255, blank=True, null=True)
    question = models.ForeignKey('Question', on_delete=models.CASCADE, blank=True, null=True, related_name='+')

    def get_absolute_url(self):
        return reverse('choice_detail',
                       kwargs={'pk': self.category.pk, 'q_pk': self.question.pk, 'c_pk': self.pk})

    def get_create_url(self):
        return reverse('choice_create', kwargs={'pk': self.category.pk, 'q_pk': self.question.pk})

    def get_delete_url(self):
        return reverse('choice_delete',
                       kwargs={'pk': self.question.category.pk, 'q_pk': self.question.pk, 'c_pk': self.pk})

    def __str__(self):
        return str(self.title)


class AnswerNumber(models.Model):
    """Модель для объединения ответов"""

    class Meta:
        verbose_name = 'Номер ответа'
        verbose_name_plural = 'Номера ответов'

    number = models.IntegerField()

    def __str__(self):
        return str(self.pk)

    def get_create_url(self):
        return reverse('answer_number_create', kwargs={'pk': self.category.pk})


class Answer(models.Model):
    """Модель для ответов пользователя"""
    class Meta:
        verbose_name = 'Ответы пользователя'
        verbose_name_plural = 'Ответы пользователей'

    answer_numbers = models.ForeignKey('AnswerNumber', on_delete=models.DO_NOTHING)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    answer_text = models.TextField('Ответ Текстом', blank=True, null=True)
    answer_choice = models.ForeignKey(Choice, on_delete=models.CASCADE, blank=True, null=True,
                                      related_name='answer_choice')
    answer_multi = models.ManyToManyField(Choice, blank=True, related_name='answer_multi')

    def get_absolute_url(self):
        return reverse('answer_list', kwargs={'pk': self.category.pk, 'an_pk': self.answernumber.pk})

    def get_create_url(self):
        return reverse('answer_create', kwargs={'pk': self.category.pk, 'q_pk': self.question.pk, 'an_pk': self.answer_numbers})

    def __str__(self):
        return '№-{}. Опрос: {}, вопрос: {}'.format(self.answer_numbers, self.category.title, self.question.title)
