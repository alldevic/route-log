from django.db import models
import os
from django.utils.text import slugify


def get_file_path(instance, filename):
    name, ext = os.path.splitext(filename)
    return os.path.join('files', slugify(name, allow_unicode=True) + ext)


class Document(models.Model):
    description = models.CharField(max_length=255, blank=True)
    document = models.FileField(upload_to=get_file_path)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        """Meta definition for Document."""
        verbose_name = 'Document'
        verbose_name_plural = 'Documents'

    def __str__(self):
        """Unicode representation of Document."""
        return str(self.document)


class P2Document(models.Model):
    """Model definition for P2Document."""
    document = models.ForeignKey(Document,
                                 on_delete=models.CASCADE,
                                 verbose_name="document",
                                 related_name="p2documents",)

    description = models.CharField(max_length=150,
                                   blank=True,
                                   null=True)

    class Meta:
        """Meta definition for P2Document."""

        verbose_name = 'P2Document'
        verbose_name_plural = 'P2Documents'

    def __str__(self):
        return self.document

    def save(self):
        """Save method for P2Document."""
        pass

    def get_absolute_url(self):
        """Return absolute url for P2Document."""
        return ('')

    # TODO: Define custom methods here


class RequestDocument(models.Model):
    """Model definition for RequestDocument."""

    document = models.ForeignKey(Document,
                                 on_delete=models.CASCADE,
                                 verbose_name="document",
                                 related_name="reqsdocs",)

    description = models.CharField(max_length=255,
                                   blank=True,
                                   null=True)

    class Meta:
        """Meta definition for RequestDocument."""

        verbose_name = 'RequestDocument'
        verbose_name_plural = 'RequestDocuments'

    def __str__(self):
        """Unicode representation of RequestDocument."""
        pass

    def save(self):
        """Save method for RequestDocument."""
        pass

    def get_absolute_url(self):
        """Return absolute url for RequestDocument."""
        return ('')

    # TODO: Define custom methods here


class ReTimeDocument(models.Model):
    """Model definition for ReTimeDocument."""

    # TODO: Define fields here

    class Meta:
        """Meta definition for ReTimeDocument."""

        verbose_name = 'ReTimeDocument'
        verbose_name_plural = 'ReTimeDocuments'

    def __str__(self):
        """Unicode representation of ReTimeDocument."""
        pass

    def save(self):
        """Save method for ReTimeDocument."""
        pass

    def get_absolute_url(self):
        """Return absolute url for ReTimeDocument."""
        return ('')

    # TODO: Define custom methods here


class AdditionalExportDocument(models.Model):
    """Model definition for AdditionalExportDocument."""

    # TODO: Define fields here

    class Meta:
        """Meta definition for AdditionalExportDocument."""

        verbose_name = 'AdditionalExportDocument'
        verbose_name_plural = 'AdditionalExportDocuments'

    def __str__(self):
        """Unicode representation of AdditionalExportDocument."""
        pass

    def save(self):
        """Save method for AdditionalExportDocument."""
        pass

    def get_absolute_url(self):
        """Return absolute url for AdditionalExportDocument."""
        return ('')

    # TODO: Define custom methods here


class Report(models.Model):
    """Model definition for Report."""

    created = models.DateTimeField(
        "Created", auto_now=True, auto_now_add=False)

    p2document = models.ForeignKey(P2Document,
                                   on_delete=models.CASCADE,
                                   verbose_name="p2document",
                                   related_name="reports",)

    request_document = models.ForeignKey(RequestDocument,
                                         on_delete=models.CASCADE,
                                         verbose_name="request_document",
                                         related_name="reports",)

    re_time_document = models.ForeignKey(ReTimeDocument,
                                         on_delete=models.CASCADE,
                                         verbose_name="re_time_document",
                                         related_name="reports",)

    additional_export_document = models.ForeignKey(AdditionalExportDocument,
                                                   on_delete=models.CASCADE,
                                                   verbose_name="add_ex_do",
                                                   related_name="reports",)

    class Meta:
        """Meta definition for Report."""

        verbose_name = 'Report'
        verbose_name_plural = 'Reports'

    def __str__(self):
        """Unicode representation of Report."""
        return str(self.created)

    def save(self):
        """Save method for Report."""
        pass

    def get_absolute_url(self):
        """Return absolute url for Report."""
        return ('')

    # TODO: Define custom methods here


class Car(models.Model):
    pass


class Driver(models.Model):
    pass


class Point(models.Model):
    pass


class GeoZone(models.Model):
    pass
