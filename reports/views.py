from rest_framework import generics, viewsets, views, mixins
from rest_framework.permissions import IsAuthenticated

from reports.models import ContainerType, ContainerUnloadFact, Report
from reports.serializers import (
    ContainerTypeListSerializer,
    ContainerUnloadFactSerializer,
    GenerateReportSerializer,
    ReportSerializer)
from reports.filter import ContainerUnloadFactFilter
from django.http import HttpResponse
import xlsxwriter
import io


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
        workbook = xlsxwriter.Workbook(output, {
            'strings_to_numbers': True,
            'strings_to_formulas': True,
            'strings_to_urls': True,
            'remove_timezone': True
        })
        date_format = workbook.add_format(
            {'num_format': 'dd/mm/yy hh:MM'})
        merge_format = workbook.add_format({'align': 'center',
                                            'valign': 'vcenter'})
        merge_format.set_text_wrap()

        worksheet = workbook.add_worksheet("ЭкоГрад")
        worksheet.merge_range('A1:M2', '', merge_format)
        worksheet.merge_range(
            'A3:M3', 'Маршрутный журнал мусоровоза', merge_format)
        worksheet.write_string('A4', "Дата")
        worksheet.write_string('A5', "Наименование организации")
        worksheet.write_string('A6', "Реквизиты организации")
        worksheet.write_string(
            'A7', "Номер договора на оказание услуг по сбору и транспортированию")
        worksheet.write_string('A8', 'Контактные данные')
        worksheet.write_string(
            'A9', 'Марка, модель, регистрационный знак мусоровоза')
        worksheet.write_string(
            'A10', 'Вместимость кузова по данным технической документации, куб.м.')
        worksheet.write_string(
            'A11', 'Коэффициент уплотнения по данным технической документации')
        worksheet.write_string('A12', 'ФИО водителя')
        worksheet.write_string(
            'A13', 'Наименование организации, предоставляющей услуги ГЛОНАСС/GPS мониторинга')
        worksheet.write_string(
            'A14', 'Обозначение объекта мониторинга (автомобиля) в системе ГЛОНАСС/GPS')

        base_num = 15
        worksheet.merge_range(
            f'A{base_num}:A{base_num+1}', '№ рейса', merge_format)
        worksheet.merge_range(
            f'B{base_num}:B{base_num+1}', 'трек (маршрут) в системе мониторинга', merge_format)
        worksheet.merge_range(
            f'D{base_num}:D{base_num+1}', 'наименование отходообразвоателя', merge_format)
        worksheet.merge_range(
            f'E{base_num}:E{base_num+1}', 'место загрузки (адрес контейнерной площадки)', merge_format)
        worksheet.merge_range(
            f'F{base_num}:F{base_num+1}', 'тип контейнера (объем), куб.м.', merge_format)
        worksheet.merge_range(
            f'G{base_num}:G{base_num+1}', 'время заезда на контейнерную площадку', merge_format)
        worksheet.merge_range(
            f'H{base_num}:H{base_num+1}', 'кол-во загруженных контейнеров, шт', merge_format)
        worksheet.merge_range(
            f'I{base_num}:I{base_num+1}', 'объем собранных ТКО, куб.м.', merge_format)
        worksheet.merge_range(
            f'J{base_num}:J{base_num+1}', 'место выгрузки (наименование полигона)', merge_format)
        worksheet.merge_range(
            f'K{base_num}:L{base_num}', 'Время', merge_format)
        worksheet.write_string(f'K{base_num+1}', 'въезда на полигон')
        worksheet.write_string(f'L{base_num+1}', 'выезда с полигона')
        worksheet.merge_range(
            f'M{base_num}:M{base_num+1}', 'Вес доставленных отходов, тн', merge_format)
        worksheet.merge_range(
            f'N{base_num}:N{base_num+1}', 'примечания (причины отклонений и т.д.)', merge_format)

        base_num = 16
        for i in range(14):
            worksheet.write_number(base_num, i, i+1)

        base_num = 17
        data = ContainerUnloadFact.objects.filter(report=id)
        for row_num, row in enumerate(data):
            worksheet.write_string(base_num + row_num, 4, str(row))
            worksheet.write_number(base_num + row_num, 5, float(row.value))
            worksheet.write_datetime(
                base_num + row_num, 6, row.datetime_entry, date_format)
            worksheet.write_number(base_num + row_num, 7, row.count)
            worksheet.write_number(base_num + row_num, 8,
                                   float(row.value) * row.count)

        base_num += len(data) + 1

        worksheet.write_string(
            base_num, 1, "ФИО, подпись  и телефон ответственного за заполнение")

        worksheet.write_string(base_num + 2, 1, 'ФИО, подпись  водителя')

        workbook.close()

        output.seek(0)

        filename = f'{id}-django_simple.xlsx'
        response = HttpResponse(
            output,
            content_type='application/vnd.ms-excel'
        )
        response['Content-Disposition'] = f'attachment; filename={filename}'
        return response
