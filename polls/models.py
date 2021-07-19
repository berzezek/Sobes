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

TYPE_ANSWER = (
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
    type_answer = models.CharField('Вариант ответа', max_length=1, choices=TYPE_ANSWER)

    def __str__(self):
        return self.title_question


class Answer(models.Model):

    class Meta:
        verbose_name = 'Ответ'
        verbose_name_plural = 'Ответы'

    question = models.OneToOneField(Question, on_delete=models.CASCADE)
    answer_choice_type = models.OneToOneField('AnswerChoices', verbose_name='Выбор', on_delete=models.CASCADE, null=True, blank=True)
    answer_multi_type = models.OneToOneField('AnswerMulties', verbose_name='Мульти', on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return str(self.question)


class AnswerChoiceType(models.Model):

    class Meta:
        verbose_name = 'Ответ выбором'
        verbose_name_plural = 'Ответы выбором'

    answerchoicetype_title = models.CharField('Наименование выбора', max_length=255, blank=True, null=True)
    answerchoicetype_choice = models.ForeignKey('AnswerChoices', on_delete=models.CASCADE)

    def __str__(self):
        return self.answerchoicetype_title


class AnswerChoices(models.Model):

    answer_choices = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return '{}-{}'.format(self.answer_choices, self.pk)


class AnswerMultiType(models.Model):

    class Meta:
        verbose_name = 'Ответ опция'
        verbose_name_plural = 'Ответы опцией'

    answermultitype_title = models.CharField('Наименование выбора', max_length=255, blank=True, null=True)
    answermultitype_choice = models.ForeignKey('AnswerMulties', on_delete=models.CASCADE)

    def __str__(self):
        return self.answermultitype_title


class AnswerMulties(models.Model):

    answer_multi = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return '{}-{}'.format(self.answer_multi, self.pk)


'''Пользовательская модель'''


class UserAnswer(models.Model):

    user_name = models.OneToOneField(User, on_delete=models.DO_NOTHING)
    user_poll = models.ForeignKey(Poll, on_delete=models.DO_NOTHING)
    user_question = models.ForeignKey(Question, on_delete=models.DO_NOTHING)
    user_answer_text = models.TextField('Ответ Текстом')
    user_answer = models.ForeignKey(AnswerChoiceType, on_delete=models.DO_NOTHING)
    user_answer_multi = models.ManyToManyField(AnswerMultiType)

    def __str__(self):
        return 'Пользователь: {}, Опрос: {} - {}'.format(self.user_name, self.user_poll, self.user_question)