from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

from nav_client.serializers import DeviceSerializer
from nav_client.models import Device, SyncDate


class DeviceListView(generics.ListAPIView):
    """
    Список машин
    """
    queryset = Device.objects.filter(sync_date=SyncDate.objects.last())
    serializer_class = DeviceSerializer
    permission_classes = (IsAuthenticated,)
