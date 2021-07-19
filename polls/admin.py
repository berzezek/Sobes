from django.contrib import admin
from .models import *


class AnswerChoiceTypeInLine(admin.TabularInline):
    model = AnswerChoiceType
    # raw_id_fields = ('answer_choices',)
    # fieldsets = ['answer_choice',]


class AnswerChoiceAdmin(admin.ModelAdmin):
    inlines = [
        AnswerChoiceTypeInLine,
    ]


class AnswerMultiTypeInLine(admin.TabularInline):
    model = AnswerMultiType
    # raw_id_fields = ('answer_choices',)


class AnswerMultiAdmin(admin.ModelAdmin):
    inlines = [
        AnswerMultiTypeInLine,
    ]


admin.site.register(Poll)
admin.site.register(Question)
admin.site.register(Answer)
admin.site.register(AnswerChoiceType)
admin.site.register(AnswerChoices, AnswerChoiceAdmin)
admin.site.register(AnswerMulties, AnswerMultiAdmin)
admin.site.register(UserAnswer)
