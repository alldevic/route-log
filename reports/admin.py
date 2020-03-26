from django.contrib import admin
from import_export.admin import ImportExportActionModelAdmin

from reports.models import (
    Report,
    ContainerUnloadFact,
    ContainerType,
    Organization)


class ContainerUnloadInline(admin.StackedInline):
    model = ContainerUnloadFact


@admin.register(Report)
class ReportsAdmin(admin.ModelAdmin):
    inlines = [ContainerUnloadInline]


@admin.register(ContainerUnloadFact)
class ContainerUnloadFactAdmin(admin.ModelAdmin):
    pass


@admin.register(ContainerType)
class ContainerTypeAdmin(ImportExportActionModelAdmin):
    list_display = ('material', 'volume', 'upload_time')


@admin.register(Organization)
class OrganizationAdmin(ImportExportActionModelAdmin):
    pass
