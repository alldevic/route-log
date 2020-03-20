from django.db import models
from nav_client.models import Device, GeoZone, FlatTableRow


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
        ordering = ['-date']
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
    track_points = models.ManyToManyField(
        FlatTableRow, verbose_name='Точки маршрута')

    datetime_entry = models.DateTimeField('Время въезда', null=True)
    datetime_exit = models.DateTimeField('Время выезда', null=True)
    is_unloaded = models.BooleanField('Отгружено')
    value = models.CharField('Объем контейнера', max_length=500)
    container_type = models.CharField('Тип контейнера', max_length=500)
    directory = models.CharField('Муниципальное образование', max_length=500)
    count = models.IntegerField('Количество отгрузок')
    nav_mt_id = models.IntegerField('Код площадки в МТ', blank=True, null=True)

    def __str__(self):
        return str(self.geozone)

    class Meta:
        verbose_name = 'Факт отгрузки'
        verbose_name_plural = 'Факты отгрузки'


class Organization(models.Model):
    """Model definition for Organization."""

    name = models.CharField("Наименование оранизации", max_length=250)
    details = models.CharField('Реквизиты организации', max_length=500)
    contacts = models.CharField('Контактные данные', max_length=250)

    class Meta:
        """Meta definition for Organization."""

        verbose_name = 'Организация'
        verbose_name_plural = 'Организации'

    def __str__(self):
        """Unicode representation of Organization."""
        return self.name


class ContainerType(models.Model):
    """Model definition for ContainerType."""

    material = models.CharField("Материал контейнера", max_length=50)
    volume = models.CharField("Объем контейнера", max_length=7)
    upload_time = models.IntegerField("Время на отгрузку в секундах",
                                      default=30)

    class Meta:
        """Meta definition for ContainerType."""

        verbose_name = 'Тип контейнера'
        verbose_name_plural = 'Типы контейнеров'

    def __str__(self):
        """Unicode representation of ContainerType."""
        return f"{self.volume} {self.material}"
