from django.db import models
from django.utils import timezone
from route_log_prj import settings
import pytz


class SyncDate(models.Model):
    datetime = models.DateTimeField("Дата синхронизации",
                                    default=timezone.localtime,
                                    auto_now=False,
                                    auto_now_add=False)

    class Meta(object):
        verbose_name = "дата синхронизации"
        verbose_name_plural = "даты синхронизации"
        get_latest_by = "datetime"

    def __str__(self):
        if settings.USE_TZ:
            tz = pytz.timezone(settings.TIME_ZONE)
            return str(self.datetime.astimezone(tz))
        else:
            return str(self.datetime)


class Device(models.Model):
    sync_date = models.ForeignKey(SyncDate,
                                  on_delete=models.CASCADE,
                                  verbose_name="дата синхронизации",
                                  related_name="devices",)

    name = models.CharField("name",
                            max_length=150,
                            blank=True,
                            null=True)

    reg_number = models.CharField("regNumber",
                                  max_length=150,
                                  blank=True,
                                  null=True)

    serial_number = models.CharField("serialNumber",
                                     max_length=150,
                                     blank=True,
                                     null=True)

    garage_number = models.CharField("garageNumber",
                                     max_length=150,
                                     blank=True,
                                     null=True)

    phone = models.CharField("phone",
                             max_length=150,
                             blank=True,
                             null=True)

    sim_number = models.CharField("simNumber",
                                  max_length=150,
                                  blank=True,
                                  null=True)

    fuel_sort = models.CharField("fuelSort",
                                 max_length=150,
                                 blank=True,
                                 null=True)

    brand = models.CharField("brand",
                             max_length=150,
                             blank=True,
                             null=True)

    description = models.CharField("description",
                                   max_length=150,
                                   blank=True,
                                   null=True)

    group_ids = models.CharField("groupIds",
                                 max_length=150,
                                 blank=True,
                                 null=True)

    nav_id = models.CharField("id",
                              max_length=150,
                              blank=True,
                              null=True)

    class Meta(object):
        verbose_name = "автомобиль"
        verbose_name_plural = "автомобили"

    def __str__(self):
        return self.reg_number or self.name


class Driver(models.Model):
    sync_date = models.ForeignKey(SyncDate,
                                  on_delete=models.CASCADE,
                                  verbose_name="дата синхронизации",
                                  related_name="drivers",)

    fname = models.CharField("fname",
                             max_length=150,
                             blank=True,
                             null=True)

    mname = models.CharField("mname",
                             max_length=150,
                             blank=True,
                             null=True)

    lname = models.CharField("lname",
                             max_length=150,
                             blank=True,
                             null=True)

    licence_nr = models.CharField("licenceNr",
                                  max_length=150,
                                  blank=True,
                                  null=True)

    phone = models.CharField("phone",
                             max_length=150,
                             blank=True,
                             null=True)

    category = models.CharField("category",
                                max_length=150,
                                blank=True,
                                null=True)

    internal_nr = models.CharField("internalNr",
                                   max_length=150,
                                   blank=True,
                                   null=True)

    driver_cat = models.CharField("driverCat",
                                  max_length=150,
                                  blank=True,
                                  null=True)

    nav_id = models.CharField("id",
                              max_length=150,
                              blank=True,
                              null=True)

    class Meta(object):
        verbose_name = "водитель"
        verbose_name_plural = "водители"

    def __str__(self):
        return f"{self.lname} {self.fname} {self.mname}"


class Point(models.Model):
    sync_date = models.ForeignKey(SyncDate,
                                  on_delete=models.CASCADE,
                                  verbose_name="дата синхронизации",
                                  related_name="points",)

    lon = models.CharField("lon",
                           max_length=20,
                           blank=True,
                           null=True)

    lat = models.CharField("lat",
                           max_length=20,
                           blank=True,
                           null=True)

    class Meta(object):
        verbose_name = "точка"
        verbose_name_plural = "точки"

    def __str__(self):
        return f"{self.lat} {self.lon}"


class GeoZone(models.Model):
    sync_date = models.ForeignKey(SyncDate,
                                  on_delete=models.CASCADE,
                                  verbose_name="дата синхронизации",
                                  related_name="geozones",)

    is_custom = models.BooleanField("Является кастомной",
                                    default=False)

    name = models.CharField("name",
                            max_length=150,
                            blank=True,
                            null=True)

    points = models.ManyToManyField(Point,
                                    verbose_name="Точки")

    nav_id = models.CharField("nav_id",
                              max_length=150,
                              blank=True,
                              null=True)

    mt_id = models.IntegerField("mt_id",
                                blank=True,
                                null=True)

    class Meta(object):
        verbose_name = "геозона"
        verbose_name_plural = "геозоны"

    def __str__(self):
        return self.name


class FlatTableRow(models.Model):
    sync_date = models.ForeignKey(SyncDate,
                                  on_delete=models.CASCADE,
                                  verbose_name="дата синхронизации",
                                  related_name="flattablerows",)

    device = models.ForeignKey(Device,
                               on_delete=models.CASCADE,
                               verbose_name="автомобиль",
                               related_name="flattablerows",
                               null=True)

    utc = models.CharField("utc",
                           max_length=150,
                           blank=True,
                           null=True)

    point_value = models.ForeignKey(Point,
                                    on_delete=models.CASCADE,
                                    verbose_name="точка",
                                    related_name="flattablerows",)

    class Meta(object):
        verbose_name = "FlatTableRow"
        verbose_name_plural = "FlatTableRows"

    def __str__(self):
        return self.utc


class FlatTable(models.Model):
    sync_date = models.ForeignKey(SyncDate,
                                  on_delete=models.CASCADE,
                                  verbose_name="дата синхронизации",
                                  related_name="flattables",)

    ts = models.CharField("ts",
                          max_length=150,
                          blank=True,
                          null=True)

    rows = models.ManyToManyField(FlatTableRow,
                                  verbose_name="FlatTableRows")

    class Meta(object):
        verbose_name = "FlatTable"
        verbose_name_plural = "FlatTables"

    def __str__(self):
        return self.ts


class NavMtId(models.Model):
    sync_date = models.ForeignKey(SyncDate,
                                  on_delete=models.CASCADE,
                                  verbose_name="дата синхронизации",
                                  related_name="navmtids",)

    name = models.CharField("name",
                            max_length=150,
                            blank=True,
                            null=True)

    nav_id = models.IntegerField("nav_id")

    mt_id = models.IntegerField("mt_id",
                                blank=True,
                                null=True)

    class Meta(object):
        verbose_name = "площадка МТ"
        verbose_name_plural = "площадки МТ"

    def __str__(self):
        return self.name


class NavRoute(models.Model):
    sync_date = models.ForeignKey(SyncDate,
                                  on_delete=models.CASCADE,
                                  verbose_name="дата синхронизации",
                                  related_name="routes",)

    nav_id = models.IntegerField("nav_id")

    name = models.CharField("name",
                            max_length=150,
                            null=True,
                            blank=True)

    from_utc = models.CharField("from_utc",
                                max_length=150,
                                null=True,
                                blank=True)

    to_utc = models.CharField("to_utc",
                              max_length=150,
                              null=True,
                              blank=True)

    nav_device_id = models.IntegerField("nav_device_id",
                                        null=True,
                                        blank=True)

    nav_driver_id = models.IntegerField("nav_driver_id",
                                        null=True,
                                        blank=True)

    class Meta(object):
        verbose_name = "маршрут навигации"
        verbose_name_plural = "маршруты навигации"

    def str(self):
        return self.name
