from django.contrib import admin
from import_export.admin import ImportExportActionModelAdmin

from .models import SyncDate, Device, Driver, Point, GeoZone, \
    FlatTableRow, FlatTable, NavMtId


class InputFilter(admin.SimpleListFilter):
    template = 'admin/input_filter.html'

    def lookups(self, request, model_admin):
        # Dummy, required to show the filter.
        return ((),)

    def choices(self, changelist):
        # Grab only the "all" option.
        all_choice = next(super().choices(changelist))
        all_choice['query_parts'] = (
            (k, v)
            for k, v in changelist.get_filters_params().items()
            if k != self.parameter_name
        )
        yield all_choice


class MtIdFilter(InputFilter):
    parameter_name = 'mt_id'
    title = 'Идентификатор МТ'

    def queryset(self, request, queryset):
        if self.value() is not None:
            mt_id = self.value()
            return queryset.filter(mt_id=mt_id)


class NavIdFilter(InputFilter):
    parameter_name = 'nav_id'
    title = 'Идентификатор навигации'

    def queryset(self, request, queryset):
        if self.value() is not None:
            nav_id = self.value()
            return queryset.filter(nav_id=nav_id)


@admin.register(Device)
class DeviceAdmin(ImportExportActionModelAdmin):
    list_display = ('name', 'sync_date')
    list_filter = ('sync_date', NavIdFilter)


@admin.register(Driver)
class DriverAdmin(ImportExportActionModelAdmin):
    list_display = ('lname', 'fname', 'mname', 'sync_date')
    list_filter = ('sync_date', NavIdFilter)


@admin.register(SyncDate)
class SyncDateAdmin(admin.ModelAdmin):
    pass


@admin.register(Point)
class PointAdmin(ImportExportActionModelAdmin):
    list_display = ('sync_date', 'lat', 'lon')
    list_filter = ('sync_date',)


@admin.register(GeoZone)
class GeoZoneAdmin(ImportExportActionModelAdmin):
    list_display = ('name', 'mt_id', 'sync_date')
    list_filter = ('sync_date', MtIdFilter,  NavIdFilter)
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
    list_display = ('name', 'mt_id', 'sync_date')
    list_filter = ('sync_date', MtIdFilter,  NavIdFilter)
