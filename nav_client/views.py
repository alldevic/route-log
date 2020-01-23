from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

from nav_client.serializers import DeviceSerializer
from nav_client.models import Device


class DeviceListView(generics.ListAPIView):
    """
    Список машин
    """
    queryset = Device.objects.all()
    serializer_class = DeviceSerializer
    permission_classes = (IsAuthenticated,)
