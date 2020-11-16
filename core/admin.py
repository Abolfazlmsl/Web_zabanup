from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as UserAdminBase
from django.utils.translation import gettext as _

from core import models

# Register your models here.


class UserAdmin(UserAdminBase):
    ordering = ['id']
    list_display = ['phone_number', 'name']
    fieldsets = (
        (None, {'fields': ('phone_number', 'password')}),
        (
            _('Personal Info'),
            {
                'fields': (
                    'name',
                    'email',
                    'generated_token',
                    'is_verified',
                    'picture',
                    'gender',
                )
            }
        ),
        (
            _('Permissions'),
            {
                'fields': ('is_active', 'is_staff', 'is_superuser', 'groups')
            }
        ),
        (
            _('Important dates'),
            {
                'fields': ('last_login',)
            }
        )
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('phone_number', 'password1', 'password2')
        }),
    )


admin.site.register(models.User, UserAdmin)
admin.site.register(models.Book)
admin.site.register(models.Category)
admin.site.register(models.Exam)
admin.site.register(models.Reading)
admin.site.register(models.Question)
admin.site.register(models.Answer)
admin.site.register(models.UserAnswer)
admin.site.register(models.Comment)
admin.site.register(models.Ticket)
admin.site.register(models.TicketMessage)
admin.site.register(models.Chat)
admin.site.register(models.ChatMessage)
