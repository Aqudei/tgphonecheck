from django.contrib import admin
from phonechecker.models import *
# Register your models here.


@admin.register(Check)
class CheckAdmin(admin.ModelAdmin):
    list_display = ('timestamp', 'phone_number', 'result')


@admin.register(PhoneNumber)
class PhoneNumberAdmin(admin.ModelAdmin):
    list_display = ('phone_number',)


@admin.register(BotLogin)
class BotLoginAdmin(admin.ModelAdmin):
    list_display = ('batch', 'done', 'phone_number', 'code', 'two_factor')


@admin.register(Upload)
class UploadAdmin(admin.ModelAdmin):
    list_display = ('phone_column', 'file', 'remarks', 'batch_id')
