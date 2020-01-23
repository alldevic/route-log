from rest_framework import serializers

from nav_client.models import Point, GeoZone, Device


class PointSerializer(serializers.ModelSerializer):
    class Meta:
        model = Point
        fields = (
            'lat',
            'lon',
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
