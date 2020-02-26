from rest_framework import serializers

from nav_client.models import Device, SyncDate
from nav_client.serializers import (
    DeviceSerializer,
    FlatRowSerializer,
    GeozoneSerializer,
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


try:
    last_sync_date = SyncDate.objects.last()
except Exception:
    last_sync_date = SyncDate.objects.all()


class GenerateReportSerializer(serializers.ModelSerializer):
    device = serializers.PrimaryKeyRelatedField(
        queryset=Device.objects.filter(
            sync_date=last_sync_date))
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
        date = validated_data.get('date', None)
        device = validated_data.get('device', None)

        if attachment and date:
            for row in attachment_parser.parse(attachment, date, device):
                obj = ContainerUnloadFact.objects.create(report=report,
                                                         geozone=row["geozone"],
                                                         datetime_entry=row["time_in"],
                                                         datetime_exit=row["time_out"],
                                                         is_unloaded=row["is_unloaded"],
                                                         value=row["value"],
                                                         container_type=row["ct_type"],
                                                         directory=row["directory"],
                                                         count=row["count"])
                obj.track_points.set(row["track_points"])
        application = validated_data.get('application', None)
        if application:
            print('Application')

        return report


class ContainerUnloadFactSerializer(serializers.ModelSerializer):
    track_points = FlatRowSerializer(many=True, read_only=True)
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
