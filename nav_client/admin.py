from django.contrib import admin
from import_export.admin import ImportExportActionModelAdmin

from .models import Device, SyncDate


@admin.register(Device)
class DeviceAdmin(ImportExportActionModelAdmin):
    list_display = ('name', 'sync_date')
    list_filter = ('sync_date',)


@admin.register(SyncDate)
class SyncDateAdmin(admin.ModelAdmin):
    pass
