from rest_framework import serializers

from nav_client.models import Device, SyncDate
from nav_client.serializers import (
    DeviceSerializer,
    FlatRowSerializer,
    GeozoneSerializer,
)
from reports.models import ContainerType, ContainerUnloadFact, Report

from . import attachment_parser
from rest_framework.fields import SerializerMethodField


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
    container_types = serializers.ListField(required=False)

    class Meta:
        model = Report
        fields = (
            'id',
            'created_at',
            'device',
            'date',
            'attachment',
            'application',
            'container_types'
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
        container_types = validated_data.get('container_types', None)

        if attachment and date:
            bulk_obj = []
            bulk_tp = []

            for row in attachment_parser \
                    .parse(attachment, date, device, container_types):
                obj = ContainerUnloadFact(report=report,
                                          geozone=row["geozone"],
                                          datetime_entry=row["time_in"],
                                          datetime_exit=row["time_out"],
                                          is_unloaded=row["is_unloaded"],
                                          value=row["value"],
                                          container_type=row["ct_type"],
                                          directory=row["directory"],
                                          count=row["count"],
                                          nav_mt_id=row["nav_mt_id"])
                bulk_obj.append(obj)
                bulk_tp.append(row["track_points"])

            objs = ContainerUnloadFact.objects.bulk_create(bulk_obj)

            ThroughModel = ContainerUnloadFact.track_points.through
            [print(x) for x in bulk_tp]
            bulk_tr = [ThroughModel(flattablerow_id=tp.id,
                                    containerunloadfact_id=item.pk)
                       for i, item in enumerate(objs)
                       for tp in bulk_tp[i]
                       if item and tp]
            ThroughModel.objects.bulk_create(bulk_tr)

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
            'nav_mt_id',
        )


class ContainerTypeListSerializer(serializers.ModelSerializer):
    text = SerializerMethodField()

    def get_text(self, obj):
        return obj.__str__()

    class Meta:
        model = ContainerType
        fields = ('id', 'text')
