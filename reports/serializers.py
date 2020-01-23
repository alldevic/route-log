from rest_framework import serializers
from nav_client.serializers import PointSerializer, DeviceSerializer, GeozoneSerializer

from reports.models import Report, ContainerUnloadFact


class ReportSerializer(serializers.ModelSerializer):
    class Meta:
        model = Report
        fields = (
            'id',
            'created_at',
        )

    def create(self, validated_data):
        """
        TODO: Включить логику формирования отчета
        """
        return Report.objects.create()


class ContainerUnloadFactSerializer(serializers.ModelSerializer):
    track_points = PointSerializer(many=True)
    device = DeviceSerializer(many=False)
    geozone = GeozoneSerializer(many=False)

    class Meta:
        model = ContainerUnloadFact
        fields = (
            'id',
            'device',
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
