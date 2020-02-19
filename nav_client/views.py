from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

from nav_client.serializers import DeviceSerializer
from nav_client.models import Device, SyncDate


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
