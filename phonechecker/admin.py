from django.contrib import admin
from phonechecker.models import *
# Register your models here.


@admin.register(Check)
class CheckAdmin(admin.ModelAdmin):
    list_display = ('timestamp', 'phone_number', 'result',
                    'username', 'debug', 'source', 'batch')
    list_filter = ('result',)
    search_fields = ('phone_number__phone_number',
                     'username', 'batch', 'debug')


@admin.register(PhoneNumber)
class PhoneNumberAdmin(admin.ModelAdmin):
    list_display = ('phone_number',)


@admin.register(BotLogin)
class BotLoginAdmin(admin.ModelAdmin):
    list_display = ('batch', 'done', 'phone_number', 'code', 'two_factor')


@admin.register(Upload)
class UploadAdmin(admin.ModelAdmin):
    list_display = ('phone_column', 'file', 'remarks', 'batch_id')


@admin.register(MySql)
class MySqlAdmin(admin.ModelAdmin):
    list_display = ('db_name', 'db_username', 'db_password',
                    'db_host', 'db_port', 'db_table', 'db_column', 'timestamp')
