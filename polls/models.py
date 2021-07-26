from django.db import models
from django.contrib.auth.models import User
from pygments.lexers import get_lexer_by_name
from pygments.formatters.html import HtmlFormatter
from pygments import highlight


class Poll(models.Model):
    """Модель для опросов"""
    class Meta:
        verbose_name = 'Опрос'
        verbose_name_plural = 'Опросы'
        ordering = ['-start_date_poll']

    owner_poll = models.ForeignKey(User, on_delete=models.CASCADE, related_name='owner_polls')
    title_poll = models.CharField('Наименование опроса', max_length=255)
    description_poll = models.CharField('Описание опроса', max_length=255)
    start_date_poll = models.DateField('Дата начала опроса', blank=True, null=True)
    end_date_poll = models.DateField('Дата окончания опроса', blank=True, null=True)

    def __str__(self):
        return self.title_poll


class AnswerChoice(models.Model):

    """Промежуточная модель для формирования вариантов ответов"""
    answer_title = models.CharField('Варианты ответа', max_length=255, blank=True, null=True)
    answer = models.ForeignKey('Question', on_delete=models.CASCADE, blank=True, null=True, related_name='answers')

    def __str__(self):
        return "{}: {}".format(self.answer, self.answer_title)


class Question(models.Model):
    """Модель для вопросов к опросам"""
    class Meta:
        verbose_name = 'Вопрос'
        verbose_name_plural = 'Вопросы'

    TYPE_QUESTION = (
        ('1', 'Текст'),
        ('2', 'Выбор'),
        ('3', 'Опция'),
    )

    poll_question = models.ForeignKey(Poll, verbose_name='Наименование опроса',
                                      on_delete=models.CASCADE, blank=True, null=True, related_name='question_poll')
    title_question = models.CharField('Вопрос', max_length=255)
    type_question = models.CharField('Тип ответа', max_length=1, choices=TYPE_QUESTION, default='1')
    # answer_question = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return self.title_question


class UserAnswer(models.Model):
    """Модель для ответов пользователя"""
    class Meta:
        verbose_name = 'Ответы пользователя'
        verbose_name_plural = 'Ответы пользователей'

    user_name = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    user_poll = models.ForeignKey(Poll, on_delete=models.DO_NOTHING)
    user_question = models.ForeignKey(Question, on_delete=models.DO_NOTHING)
    user_answer_text = models.TextField('Ответ Текстом', blank=True, null=True)
    user_answer_choice = models.ForeignKey(AnswerChoice, on_delete=models.DO_NOTHING, blank=True, null=True, related_name='+')
    user_answer_multi = models.ManyToManyField(AnswerChoice, blank=True, related_name='+')

    def __str__(self):
        return 'Пользователь: {}, Опрос: {} - {}'.format(self.user_name, self.user_poll, self.user_question)