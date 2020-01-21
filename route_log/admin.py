from django.contrib import admin

from .models import Document, P2Document, RequestDocument, \
    ReTimeDocument, AdditionalExportDocument, Report


@admin.register(Document)
class DocumentAdmin(admin.ModelAdmin):
    pass


@admin.register(P2Document)
class P2DocumentAdmin(admin.ModelAdmin):
    pass


@admin.register(RequestDocument)
class RequestDocumentAdmin(admin.ModelAdmin):
    pass


@admin.register(ReTimeDocument)
class ReTimeDocumentAdmin(admin.ModelAdmin):
    pass


@admin.register(AdditionalExportDocument)
class AdditionalExportDocumentAdmin(admin.ModelAdmin):
    pass


@admin.register(Report)
class ReportAdmin(admin.ModelAdmin):
    pass
