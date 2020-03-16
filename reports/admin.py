from django.contrib import admin

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
class ContainerTypeAdmin(admin.ModelAdmin):
    pass


@admin.register(Organization)
class OrganizationAdmin(admin.ModelAdmin):
    pass
