from django.contrib import admin
from .models import *


class AnswerChoiceInLine(admin.TabularInline):
    model = AnswerChoice


class QuestionAdmin(admin.ModelAdmin):
    inlines = [
        AnswerChoiceInLine,
    ]


admin.site.register(Poll)
admin.site.register(Question, QuestionAdmin)
admin.site.register(UserAnswer)