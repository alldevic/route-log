from rest_framework import serializers

from nav_client.models import Point, GeoZone, Device, SyncDate, FlatTableRow, NavMtId
from rest_framework.fields import SerializerMethodField


class ArrayPointSerializer(serializers.RelatedField):
    def to_representation(self, value):
        return value.lat, value.lon

    def to_internal_value(self, data):
        return data.split(',')


class PointSerializer(serializers.ModelSerializer):
    class Meta:
        model = Point
        fields = (
            'lon',
            'lat',
        )


try:
    last_sync_date = SyncDate.objects.last()
except Exception:
    last_sync_date = SyncDate.objects.all()


class FlatRowSerializer(serializers.ModelSerializer):
    point_value = PointSerializer()

    class Meta:
        model = FlatTableRow
        fields = (
            'point_value',
            'utc'
        )


class GeozoneSerializer(serializers.ModelSerializer):
    points = ArrayPointSerializer(queryset=Point.objects.filter(
        sync_date=last_sync_date),
        many=True)

    # points = SerializerMethodField()

    # def get_points(self, obj):
    #     queryset = Point.objects.filter(sync_date=last_sync_date)
    #     res = ArrayPointSerializer(queryset, many=True)
    #     return res.data

    class Meta:
        model = GeoZone
        fields = (
            'id',
            'name',
            'points',
        )


class DeviceSerializer(serializers.ModelSerializer):

    class Meta:
        model = Device
        fields = (
            'id',
            'name',
            'reg_number',
            'serial_number',
            'garage_number',
            'phone',
            'sim_number',
            'brand',
        )


class NavMtIdSerializer(serializers.ModelSerializer):

    class Meta:
        model = NavMtId
        fields = (
            'id',
            'name',
            'mt_id',
        )
