from django.contrib import admin
from .models import *


class AnswerChoiceInLine(admin.TabularInline):
    model = AnswerChoice
    # raw_id_fields = ('answer_choices',)
    # fields = ('question_choices',)
    # extra = 3


class QuestionAdmin(admin.ModelAdmin):
    inlines = [
        AnswerChoiceInLine,
    ]
    exclude = ('question_choices', )


admin.site.register(Poll)
admin.site.register(Question, QuestionAdmin)
admin.site.register(AnswerChoice)
admin.site.register(UserAnswer)
