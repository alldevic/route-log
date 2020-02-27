from rest_framework import generics, viewsets, views, mixins
from rest_framework.permissions import IsAuthenticated

from reports.models import ContainerUnloadFact, Report
from reports.serializers import (
    ContainerUnloadFactSerializer,
    ReportSerializer,
    GenerateReportSerializer)
from reports.filter import ContainerUnloadFactFilter
from django.http import HttpResponse
import xlsxwriter
import io


class ContanerUnloadsListView(viewsets.ModelViewSet):
    """
    Список фактов отгрузки
    """
    queryset = ContainerUnloadFact.objects.all()
    serializer_class = ContainerUnloadFactSerializer
    filterset_class = ContainerUnloadFactFilter
    permission_classes = (IsAuthenticated,)


class ReportsViewSet(
    mixins.ListModelMixin,
    mixins.UpdateModelMixin,
    mixins.RetrieveModelMixin,
    viewsets.GenericViewSet
):
    queryset = Report.objects.all()
    serializer_class = ReportSerializer
    permission_classes = (IsAuthenticated,)


class GenerateReportView(generics.CreateAPIView):
    serializer_class = GenerateReportSerializer
    permission_classes = (IsAuthenticated,)


class ExportReportView(views.APIView):
    """
    Экспорт отчета в виде файла
    Id - идентификатор отчета
    """
    permission_classes = (IsAuthenticated,)

    def get(self, request, id, *args, **kwargs):
        output = io.BytesIO()
        workbook = xlsxwriter.Workbook(output)
        worksheet = workbook.add_worksheet()

        data = get_simple_table_data()

        for row_num, columns in enumerate(data):
            for col_num, cell_data in enumerate(columns):
                worksheet.write(row_num, col_num, cell_data)

        workbook.close()

        output.seek(0)

        filename = f'{id}-django_simple.xlsx'
        response = HttpResponse(
            output,
            content_type='application/vnd.ms-excel'
        )
        response['Content-Disposition'] = f'attachment; filename={filename}'

        # response = FileResponse(output)
        return response


def get_simple_table_data():
    return [['Apples', 10000, 5000, 8000, 6000],
            ['Pears', 2000, 3000, 4000, 5000],
            ['Bananas', 6000, 6000, 6500, 6000],
            ['Oranges', 500, 300, 200, 700],
            ]
