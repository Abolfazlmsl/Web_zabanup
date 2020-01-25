from django.contrib import admin
from . import models

# Register your models here.
admin.site.site_header = 'ZabanUp Admin Page'

admin.site.register(models.Profile)
admin.site.register(models.Answer)
admin.site.register(models.UserAnswer)
admin.site.register(models.Exam)
admin.site.register(models.ExamCategory)
admin.site.register(models.Comment)
admin.site.register(models.FavoriteQuestion)
admin.site.register(models.TicketMessage)
admin.site.register(models.Ticket)
admin.site.register(models.Chat)
admin.site.register(models.ChatMessage)
admin.site.register(models.Book)


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



