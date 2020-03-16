from django_filters import rest_framework

from nav_client.models import GeoZone, NavMtId


class GeozoneFilter(rest_framework.FilterSet):
    class Meta:
        model = GeoZone
        fields = {
            'name': ['contains'],
        }

class NavMtIdFilter(rest_framework.FilterSet):
    class Meta:
        model = NavMtId
        fields = {
            'nav_id': ['exact'],
        }
