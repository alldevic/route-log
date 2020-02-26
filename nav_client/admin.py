from django.contrib import admin
from import_export.admin import ImportExportActionModelAdmin

from .models import SyncDate, Device, Driver, Point, GeoZone, \
    FlatTableRow, FlatTable, NavMtId


@admin.register(Device)
class DeviceAdmin(ImportExportActionModelAdmin):
    list_display = ('name', 'sync_date')
    list_filter = ('sync_date',)


@admin.register(Driver)
class DriverAdmin(ImportExportActionModelAdmin):
    list_display = ('lname', 'fname', 'mname', 'sync_date')
    list_filter = ('sync_date',)


@admin.register(SyncDate)
class SyncDateAdmin(admin.ModelAdmin):
    pass


@admin.register(Point)
class PointAdmin(ImportExportActionModelAdmin):
    list_display = ('sync_date', 'lat', 'lon')
    list_filter = ('sync_date',)


@admin.register(GeoZone)
class GeoZoneAdmin(ImportExportActionModelAdmin):
    list_display = ('name', 'sync_date')
    list_filter = ('sync_date',)
    filter_horizontal = ("points",)


@admin.register(FlatTableRow)
class FlatTableRowAdmin(ImportExportActionModelAdmin):
    list_display = ('device', 'utc', 'sync_date')
    list_filter = ('sync_date',)


@admin.register(FlatTable)
class FlatTableAdmin(ImportExportActionModelAdmin):
    list_display = ('ts', 'sync_date')
    list_filter = ('sync_date',)
    filter_horizontal = ("rows",)


@admin.register(NavMtId)
class NavMtIdAdmin(ImportExportActionModelAdmin):
    list_display = ('name', 'sync_date')
    list_filter = ('sync_date',)
