from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

from nav_client.serializers import (
    DeviceSerializer,
    GeozoneSerializer,
    NavMtIdSerializer)
from nav_client.models import (Device,
                               SyncDate,
                               GeoZone,
                               NavMtId)
from nav_client.filter import GeozoneFilter, NavMtIdFilter

from datetime import datetime
from rest_framework.response import Response

try:
    last_sync_date = SyncDate.objects.last()
except Exception:
    last_sync_date = SyncDate.objects.all()


class DeviceListView(generics.ListAPIView):
    """
    Список машин
    """
    # queryset = Device.objects.filter(sync_date=last_sync_date)
    serializer_class = DeviceSerializer
    permission_classes = (IsAuthenticated,)

    def list(self, request, *args, **kwargs):

        if request.query_params.get("date", None):
            dt = datetime.strptime(
                request.query_params["date"], "%Y-%m-%d")
            sync_date = SyncDate.objects.filter(datetime__year=dt.year,
                                                datetime__month=dt.month,
                                                datetime__day=dt.day).first()
            queryset = Device.objects.filter(sync_date=sync_date)
        else:
            sync_date = last_sync_date.datetime
            queryset = Device.objects.filter(sync_date=last_sync_date)

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.paginator.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


class GeozoneListView(generics.ListAPIView):
    """
    Список площадок(муниципальных образований)
    """
    # queryset = GeoZone.objects.all(sync_date=last_sync_date)
    serializer_class = GeozoneSerializer
    filterset_class = GeozoneFilter
    permission_classes = (IsAuthenticated,)

    def list(self, request, *args, **kwargs):
        if request.query_params["date"]:
            dt = datetime.strptime(
                request.query_params["date"], "%Y-%m-%d")
            sync_date = SyncDate.objects.filter(datetime__year=dt.year,
                                                datetime__month=dt.month,
                                                datetime__day=dt.day).first()

            queryset = GeoZone.objects.filter(sync_date=sync_date)
        else:
            queryset = GeoZone.objects.filter(sync_date=last_sync_date)

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.paginator.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


class NavMtIdListView(generics.ListAPIView):
    """
    Список площадок из МТ
    """
    # queryset = NavMtId.objects.filter(sync_date=last_sync_date)
    serializer_class = NavMtIdSerializer
    filterset_class = NavMtIdFilter
    permission_classes = (IsAuthenticated,)

    def list(self, request, *args, **kwargs):
        if request.query_params["date"]:
            dt = datetime.strptime(
                request.query_params["date"], "%Y-%m-%d")
            sync_date = SyncDate.objects.filter(datetime__year=dt.year,
                                                datetime__month=dt.month,
                                                datetime__day=dt.day).first()

            queryset = NavMtId.objects.filter(sync_date=sync_date)
        else:
            queryset = NavMtId.objects.filter(sync_date=last_sync_date)

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.paginator.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
