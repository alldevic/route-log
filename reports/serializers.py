from django.utils import timezone

from rest_framework import serializers

from nav_client.models import Device, SyncDate
from nav_client.serializers import (DeviceSerializer, GeozoneSerializer,
                                    PointSerializer)
from reports.models import ContainerUnloadFact, Report

from . import attachment_parser


class ReportSerializer(serializers.ModelSerializer):
    device = DeviceSerializer(many=False)

    class Meta:
        model = Report
        fields = (
            'id',
            'created_at',
            'device',
            'date',
        )


class GenerateReportSerializer(serializers.ModelSerializer):
    device = serializers.PrimaryKeyRelatedField(
        queryset=Device.objects.filter(
            sync_date=SyncDate.objects.last()))
    date = serializers.DateField()
    attachment = serializers.FileField(write_only=True, required=False)
    application = serializers.FileField(write_only=True, required=False)

    class Meta:
        model = Report
        fields = (
            'id',
            'created_at',
            'device',
            'date',
            'attachment',
            'application'
        )

    def create(self, validated_data):
        report = Report.objects.create(date=validated_data['date'],
                                       device=Device.objects.filter(
                                           nav_id=validated_data['device'])
                                       .last()
                                       )

        attachment = validated_data.get('attachment', None)
        if attachment:
            for row in attachment_parser.parse(attachment):

                ContainerUnloadFact.objects.create(report=report,
                                                   geozone=row["geozone"],
                                                   datetime_entry=timezone.now(),
                                                   datetime_exit=timezone.now(),
                                                   is_unloaded=True,
                                                   value=row["value"],
                                                   container_type=row["ct_type"],
                                                   directory=row["directory"],
                                                   count=row["count"])
                print('created')

        application = validated_data.get('application', None)
        if application:
            print('Application')

        return report


class ContainerUnloadFactSerializer(serializers.ModelSerializer):
    track_points = PointSerializer(many=True, read_only=True)
    geozone = GeozoneSerializer(many=False, read_only=True)

    class Meta:
        model = ContainerUnloadFact
        fields = (
            'id',
            'report',
            'geozone',
            'track_points',
            'datetime_entry',
            'datetime_exit',
            'is_unloaded',
            'value',
            'container_type',
            'directory',
            'count',
        )
