from django.contrib import admin
from phonechecker.models import *
from import_export import resources
from import_export.admin import ImportExportModelAdmin
from import_export.admin import ImportExportActionModelAdmin
# Register your models here.


class CheckResource(resources.ModelResource):

    class Meta:
        model = Check
        fields = ('timestamp', 'phone_number__phone_number',
                  'result', 'username', 'source')


@admin.register(Check)
class CheckAdmin(ImportExportActionModelAdmin):
    list_display = ('timestamp', 'phone_number', 'result',
                    'username', 'debug', 'source', 'batch')
    list_filter = ('result',)
    search_fields = ('phone_number__phone_number',
                     'username', 'batch', 'debug', 'source')
    resource_class = CheckResource


@admin.register(PhoneNumber)
class PhoneNumberAdmin(admin.ModelAdmin):
    list_display = ('phone_number', 'timestamp')


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
