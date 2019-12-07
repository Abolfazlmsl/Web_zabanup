from django.contrib import admin
from . import models

# Register your models here.

admin.site.register(models.Profile)
admin.site.register(models.Answer)
admin.site.register(models.UserAnswer)
admin.site.register(models.Exam)
admin.site.register(models.Comment)
admin.site.register(models.FavoriteQuestion)
admin.site.register(models.Message)


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



