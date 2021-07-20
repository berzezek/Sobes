from django.db import models
from django.contrib.auth.models import User


class Poll(models.Model):

    class Meta:
        verbose_name = 'Опрос'
        verbose_name_plural = 'Опросы'

    title_poll = models.CharField('Наименование опроса', max_length=255)
    pubdate_poll = models.DateField('Дата публикации', null=True, blank=True)
    public_poll = models.BooleanField('Опубликовать', default=False)

    def __str__(self):
        return self.title_poll


TYPE_QUESTION = (
    ('1', 'Текст'),
    ('2', 'Выбор'),
    ('3', 'Опция'),
)


class Question(models.Model):

    class Meta:
        verbose_name = 'Вопрос'
        verbose_name_plural = 'Вопросы'

    poll = models.ForeignKey(Poll, verbose_name='Наименование опроса', on_delete=models.CASCADE)
    title_question = models.CharField('Вопрос', max_length=255)
    type_question = models.CharField('Тип ответа', max_length=1, choices=TYPE_QUESTION, default='1')
    # question_choices = models.ForeignKey('AnswerChoice', on_delete=models.CASCADE, blank=True, null=True)
    question_choices = models.CharField('Варианты ответов', max_length=255, blank=True, null=True)

    def __str__(self):
        return self.title_question


class AnswerChoice(models.Model):

    answer = models.CharField(max_length=255, blank=True, null=True)
    answer_choice = models.ForeignKey(Question, on_delete=models.CASCADE, blank=True, null=True)

    def __str__(self):
        return self.answer

'''Пользовательская модель'''


class UserAnswer(models.Model):

    class Meta:
        verbose_name = 'Ответы пользователя'
        verbose_name_plural = 'Ответы пользователей'

    user_name = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    user_poll = models.ForeignKey(Poll, on_delete=models.DO_NOTHING)
    user_question = models.OneToOneField(Question, on_delete=models.DO_NOTHING)
    user_answer_text = models.TextField('Ответ Текстом', blank=True, null=True)
    user_answer_choice = models.ForeignKey(AnswerChoice, on_delete=models.DO_NOTHING, related_name='+', blank=True, null=True)
    user_answer_multi = models.ManyToManyField(AnswerChoice, blank=True, related_name='+')

    def __str__(self):
        return 'Пользователь: {}, Опрос: {} - {}'.format(self.user_name, self.user_poll, self.user_question)