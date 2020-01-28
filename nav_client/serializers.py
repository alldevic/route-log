from rest_framework import serializers

from nav_client.models import Point, GeoZone, Device


class ArrayPointSerializer(serializers.RelatedField):
    def to_representation(self, value):
        return value.lon, value.lat

    def to_internal_value(self, data):
        return data.split(',')


class PointSerializer(serializers.ModelSerializer):
    class Meta:
        model = Point
        fields = (
            'lon',
            'lat',
        )


class GeozoneSerializer(serializers.ModelSerializer):
    points = PointSerializer(many=True)

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
