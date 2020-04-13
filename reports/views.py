from rest_framework import generics, viewsets, views, mixins
from rest_framework.permissions import IsAuthenticated

from reports.models import (
    ContainerType,
    ContainerUnloadFact,
    Report,
    Organization)
from reports.serializers import (
    ContainerTypeListSerializer,
    ContainerUnloadFactSerializer,
    GenerateReportSerializer,
    ReportSerializer)
from reports.filter import ContainerUnloadFactFilter
from django.http import HttpResponse
import xlsxwriter
import io
from rest_framework.response import Response
from django.db.models import Q


class ContainerTypeListView(mixins.ListModelMixin,
                            viewsets.GenericViewSet):
    queryset = ContainerType.objects.all()
    serializer_class = ContainerTypeListSerializer
    permission_classes = (IsAuthenticated,)


class ContanerUnloadsListView(viewsets.ModelViewSet):
    """
    Список фактов отгрузки
    """
    queryset = ContainerUnloadFact.objects.all()
    serializer_class = ContainerUnloadFactSerializer
    filterset_class = ContainerUnloadFactFilter
    permission_classes = (IsAuthenticated,)

    def list(self, request, *args, **kwargs):
        report_id = int(request.query_params["report"])

        queryset = ContainerUnloadFact.objects \
            .filter(report__id=report_id) \
            .select_related("geozone") \
            .prefetch_related("track_points__point_value", "geozone__points")

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.paginator.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


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
        # TODO: refact
        report = Report.objects.filter(pk=id).first()
        device = report.device
        output = io.BytesIO()
        workbook = xlsxwriter.Workbook(output, {
            'strings_to_numbers': True,
            'strings_to_formulas': True,
            'strings_to_urls': True,
            'remove_timezone': True
        })
        workbook.formats[0].set_font_name('Times New Roman')
        workbook.formats[0].set_font_size(12)

        table_long_date_format = workbook.add_format(
            {'num_format': 'dd/mm/yy hh:MM',
             'font_name': 'Times New Roman',
             'font_size': 12,
             'border': 1})

        bold_long_date_format = workbook.add_format(
            {'num_format': 'dd/mm/yy hh:MM',
             'font_name': 'Times New Roman',
             'font_size': 12,
             'bold': True})
        bold_text_format =  workbook.add_format(
            {
             'font_name': 'Times New Roman',
             'font_size': 12,
             'bold': True}
        )
        merge_format = workbook.add_format({'align': 'center',
                                            'valign': 'vcenter',
                                            'font_name': 'Times New Roman',
                                            'font_size': 11,
                                            'border': 1})

        merge_format.set_text_wrap()

        table_cell_format = workbook.add_format({'font_name': 'Times New Roman',
                                                 'font_size': 11,
                                                 'border': 1})
        worksheet = workbook.add_worksheet("ЭкоГрад")

        # Columns settings
        worksheet.set_column('A:A', 10)
        worksheet.set_column('B:B', 17)
        worksheet.set_column('C:C', 25)
        worksheet.set_column('D:D', 30)
        worksheet.set_column('E:E', 10)
        worksheet.set_column('F:F', 30)
        worksheet.set_column('G:G', 12)
        worksheet.set_column('H:H', 12)
        worksheet.set_column('I:I', 17)
        worksheet.set_column('J:J', 15)
        worksheet.set_column('K:K', 15)
        worksheet.set_column('L:L', 15)
        worksheet.set_column('M:M', 15)
        worksheet.set_column('N:N', 15)

        worksheet.merge_range('A1:M2', '', merge_format)
        worksheet.merge_range(
            'A3:M3', 'Маршрутный журнал мусоровоза', merge_format)
        worksheet.write_string('A4', "Дата")
        worksheet.write_datetime('B4', report.date, bold_long_date_format)

        organization = Organization.objects.first()
        worksheet.write_string('A5', organization.name)
        worksheet.write_string('A6', organization.details)
        worksheet.write_string(
            'A7',
            "Номер договора на оказание услуг по сбору и транспортированию")
        worksheet.write_string('A8', organization.contacts)
        worksheet.write_string(
            'A9', 'Марка, модель, регистрационный знак мусоровоза')
        worksheet.write_string(
            'F9', device.brand or '', bold_text_format)
        worksheet.write_string(
            'A10',
            'Вместимость кузова по данным технической документации, куб.м.')
        worksheet.write_string(
            'A11', 'Коэффициент уплотнения по данным технической документации')
        worksheet.write_string('A12', 'ФИО водителя')
        worksheet.write_string(
            'A13',
            'Наименование организации, предоставляющей услуги ГЛОНАСС/GPS мониторинга')
        worksheet.write_string(
            'A14',
            'Обозначение объекта мониторинга (автомобиля) в системе ГЛОНАСС/GPS')
        worksheet.write_string(
            'F14', device.name or '', bold_text_format)
        base_num = 15
        worksheet.set_row(base_num, 40)
        worksheet.merge_range(
            f'A{base_num}:A{base_num+1}', '№ рейса', merge_format)
        worksheet.merge_range(
            f'B{base_num}:B{base_num+1}',
            'трек (маршрут) в системе мониторинга', merge_format)
        worksheet.merge_range(
            f'C{base_num}:C{base_num+1}',
            'наименование отходообразвоателя', merge_format)
        worksheet.merge_range(
            f'D{base_num}:D{base_num+1}',
            'место загрузки (адрес контейнерной площадки)', merge_format)
        worksheet.merge_range(
            f'E{base_num}:E{base_num+1}',
            'тип контейнера (объем), куб.м.', merge_format)
        worksheet.merge_range(
            f'F{base_num}:F{base_num+1}',
            'время заезда на контейнерную площадку', merge_format)
        worksheet.merge_range(
            f'G{base_num}:G{base_num+1}',
            'кол-во загруженных контейнеров, шт', merge_format)
        worksheet.merge_range(
            f'H{base_num}:H{base_num+1}',
            'объем собранных ТКО, куб.м.', merge_format)
        worksheet.merge_range(
            f'I{base_num}:I{base_num+1}',
            'место выгрузки (наименование полигона)', merge_format)
        worksheet.merge_range(
            f'J{base_num}:K{base_num}', 'Время', merge_format)
        worksheet.write_string(f'K{base_num+1}', 'въезда на полигон')
        worksheet.write_string(f'L{base_num+1}', 'выезда с полигона')
        worksheet.merge_range(
            f'L{base_num}:L{base_num+1}',
            'Вес доставленных отходов, тн', merge_format)
        worksheet.merge_range(
            f'M{base_num}:M{base_num+1}',
            'примечания (причины отклонений и т.д.)', merge_format)

        base_num = 16
        for i in range(13):
            worksheet.write_number(base_num, i, i+1, table_cell_format)

        base_num = 17
        data = ContainerUnloadFact.objects\
            .filter(report=id) \
            .exclude(datetime_entry=None, datetime_exit=None)
        for row_num, row in enumerate(data):
            worksheet.write(base_num + row_num, 0, '', table_cell_format)
            worksheet.write(base_num + row_num, 1, '', table_cell_format)
            worksheet.write(base_num + row_num, 2, '', table_cell_format)
            worksheet.write_string(base_num + row_num, 3,
                                   str(row), table_cell_format)
            worksheet.write_number(base_num + row_num, 4,
                                   float(row.value), table_cell_format)
            if row.datetime_entry:
                worksheet.write_datetime(
                    base_num + row_num, 5,
                    row.datetime_entry,
                    table_long_date_format)
            else:
                worksheet.write_string(
                    base_num + row_num, 5, "Нет данных", table_cell_format)
            worksheet.write_number(base_num + row_num, 6,
                                   row.count, table_cell_format)
            worksheet.write_number(base_num + row_num, 7,
                                   float(row.value) * row.count,
                                   table_cell_format)
            worksheet.write(base_num + row_num, 8, '', table_cell_format)
            worksheet.write(base_num + row_num, 9, '', table_cell_format)
            worksheet.write(base_num + row_num, 10, '', table_cell_format)
            worksheet.write(base_num + row_num, 11, '', table_cell_format)
            worksheet.write(base_num + row_num, 12, '', table_cell_format)

        base_num += len(data) + 1

        worksheet.write_string(
            base_num, 1,
            "ФИО, подпись  и телефон ответственного за заполнение")

        worksheet.write_string(base_num + 2, 1, 'ФИО, подпись  водителя')

        workbook.close()

        output.seek(0)

        filename = f'{report.date.year}_{report.date.month}_{report.date.day}.xlsx'
        
        response = HttpResponse(
            output,
            content_type='application/vnd.ms-excel'
        )
        response['Content-Disposition'] = f'attachment; filename={filename}'
        return response
