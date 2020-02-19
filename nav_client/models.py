from django.db import models


class SyncDate(models.Model):
    datetime = models.DateTimeField("Дата синхронизации",
                                    auto_now=True,
                                    auto_now_add=False)

    class Meta(object):
        verbose_name = "дата синхронизации"
        verbose_name_plural = "даты синхронизации"
        get_latest_by = "datetime"

    def __str__(self):
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
        verbose_name = "машина"
        verbose_name_plural = "машины"

    def __str__(self):
        return self.name


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

    name = models.CharField("name",
                            max_length=150,
                            blank=True,
                            null=True)

    points = models.ManyToManyField(Point,
                                    verbose_name="Точки")

    nav_id = models.CharField("id",
                              max_length=150,
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
