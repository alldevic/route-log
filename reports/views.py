from rest_framework import generics, viewsets, views, mixins
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from reports.models import ContainerUnloadFact, Report
from reports.serializers import ContainerUnloadFactSerializer, ReportSerializer


class ContanerUnloadsListView(generics.ListAPIView):
    """
    Список фактов отгрузки
    """
    queryset = ContainerUnloadFact.objects.all()
    serializer_class = ContainerUnloadFactSerializer
    # permission_classes = (IsAuthenticated,)


class ReportsViewSet(
    mixins.ListModelMixin,
    mixins.UpdateModelMixin,
    mixins.RetrieveModelMixin,
    viewsets.GenericViewSet
):
    queryset = Report.objects.all()
    serializer_class = ReportSerializer
    # permission_classes = (IsAuthenticated,)


class ExportReportView(views.APIView):
    # permission_classes = (IsAuthenticated,)

    def get(self):
        """
        TODO: Включить логику формирования документа по ContainerUnloadFact
        """
        return Response()
