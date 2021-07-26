from django.contrib import admin
from .models import *


class AnswerChoiceInLine(admin.TabularInline):
    model = AnswerChoice
    # fields = ('answer_question',)


class QuestionAdmin(admin.ModelAdmin):
    inlines = [
        AnswerChoiceInLine,
    ]
    exclude = ('answer_question',)


admin.site.register(Poll)
admin.site.register(Question, QuestionAdmin)
admin.site.register(UserAnswer)