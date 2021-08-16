from django.contrib import admin
from .models import Category, Question, Choice, Answer


class CategoryAdmin(admin.ModelAdmin):
    # prepopulated_fields = {"slug": ("title",)}
    fields = ('owner', 'title', 'description', 'start_date', 'end_date')


class ChoiceInline(admin.TabularInline):
    model = Choice


class QuestionAdmin(admin.ModelAdmin):
    inlines = [
        ChoiceInline,
    ]
    # prepopulated_fields = {"slug": ("title", )}



admin.site.register(Category, CategoryAdmin)
admin.site.register(Question, QuestionAdmin)
admin.site.register(Choice)
admin.site.register(Answer)

