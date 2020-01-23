from django.contrib import admin

from reports.models import Report, ContainerUnloadFact


class ContainerUnloadInline(admin.StackedInline):
    model = ContainerUnloadFact


@admin.register(Report)
class ReportsAdmin(admin.ModelAdmin):
    inlines = [ContainerUnloadInline]
