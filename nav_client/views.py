from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

from nav_client.serializers import DeviceSerializer, GeozoneSerializer, NavMtIdSerializer
from nav_client.models import Device, SyncDate, GeoZone, NavMtId
from nav_client.filter import GeozoneFilter, NavMtIdFilter

try:
    last_sync_date = SyncDate.objects.last()
except Exception:
    last_sync_date = SyncDate.objects.all()


class DeviceListView(generics.ListAPIView):
    """
    Список машин
    """
    queryset = Device.objects.filter(sync_date=last_sync_date)
    serializer_class = DeviceSerializer
    permission_classes = (IsAuthenticated,)


class GeozoneListView(generics.ListAPIView):
    """
    Список площадок(муниципальных образований)
    """
    queryset = GeoZone.objects.all()
    serializer_class = GeozoneSerializer
    filterset_class = GeozoneFilter
    # permission_classes = (IsAuthenticated,)


class NavMtIdListView(generics.ListAPIView):
    """
    Список площадок из МТ
    """
    queryset = NavMtId.objects.all()
    serializer_class = NavMtIdSerializer
    filterset_class = NavMtIdFilter
    # permission_classes = (IsAuthenticated,)
