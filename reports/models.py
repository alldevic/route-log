from django.db import models
from nav_client.models import Device, Point, GeoZone


class Report(models.Model):
    """
    Отчет, создается при загрузке приложения 2 и заявок
    """
    created_at = models.DateTimeField(auto_now_add=True)
    name = models.CharField('Наименование', max_length=500, default='Отчет')
    device = models.ForeignKey(
        Device, verbose_name='Транспорт', on_delete=models.SET_NULL, null=True)
    date = models.DateField('Дата')

    def __str__(self):
        return f'Отчет "{self.name}" за {self.date}'

    class Meta:
        verbose_name = 'Отчет'
        verbose_name_plural = 'Отчеты'


class ContainerUnloadFact(models.Model):
    """
    Факт отгрузки контейнера
    """
    report = models.ForeignKey(
        Report, verbose_name='Отчет', on_delete=models.CASCADE)
    geozone = models.ForeignKey(
        GeoZone, verbose_name='Платформа', on_delete=models.SET_NULL, null=True)
    track_points = models.ManyToManyField(Point, verbose_name='Точки маршрута')

    datetime_entry = models.DateTimeField('Время въезда')
    datetime_exit = models.DateTimeField('Время выезда')
    is_unloaded = models.BooleanField('Отгружено')
    value = models.CharField('Объем контейнера', max_length=500)
    container_type = models.CharField('Тип контейнера', max_length=500)
    directory = models.CharField('Муниципальное образование', max_length=500)
    count = models.IntegerField('Количество отгрузок')

    def __str__(self):
        return str(self.geozone)

    class Meta:
        verbose_name = 'Факт отгрузки'
        verbose_name_plural = 'Факты отгрузки'
