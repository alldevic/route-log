from django.contrib import admin

from .models import Device, SyncDate


@admin.register(Device)
class DeviceAdmin(admin.ModelAdmin):
    list_display = ('name', 'sync_date')
    list_filter = ('sync_date',)


@admin.register(SyncDate)
class SyncDateAdmin(admin.ModelAdmin):
    pass
