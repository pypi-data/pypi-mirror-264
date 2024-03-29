from django.contrib import admin
from django.contrib.admin.widgets import AdminTextInputWidget
from django.core.exceptions import ValidationError
from django.db.models import ForeignKey, OneToOneField

from . import models


@admin.register(models.Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('created', 'user_id', 'last_name', 'first_name', 'middle_name', 'birth_date',
                    'is_identified', 'is_verified', 'is_sign',
                    'passport_serial', 'passport_number', 'snils'
                    )
    search_fields = ('=user_id', '=passport_number', '=snils')
    list_filter = ('created', 'is_identified', 'is_verified', 'is_sign')
    ordering = ('-created',)
    readonly_fields = ('user_id',)

    def has_delete_permission(self, request, obj=None):
        return False

    def save_model(self, request, obj, form, change):
        try:
            super().save_model(request, obj, form, change)
        except ValidationError as e:
            self.message_user(request, str(e.message), 'ERROR')


@admin.register(models.PhoneNumber)
class PhoneNumberAdmin(admin.ModelAdmin):
    list_display = ('created', 'profile', 'is_active', 'type', 'phonenumber', 'comment',)
    search_fields = ('=profile_id', '=phonenumber')
    list_filter = ('created', 'is_active', 'type')
    ordering = ('-created',)
    readonly_fields = ('profile',)
    formfield_overrides = {
        ForeignKey: {'widget': AdminTextInputWidget},
        OneToOneField: {'widget': AdminTextInputWidget},
    }


@admin.register(models.HistoryProfile)
class HistoryProfileAdmin(admin.ModelAdmin):
    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return True
