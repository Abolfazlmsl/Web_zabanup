from django.contrib import admin
from . import models

# Register your models here.


class QuestionInline(admin.TabularInline):
    model = models.Question


@admin.register(models.Passage)
class PassageAdmin(admin.ModelAdmin):
    list_filter = ('title', 'id')
    inlines = [QuestionInline]


class AnswerInline(admin.TabularInline):
    model = models.Answer
    extra = 0


@admin.register(models.Question)
class QuestionAdmin(admin.ModelAdmin):
    list_filter = ('id',)
    inlines = [AnswerInline]




