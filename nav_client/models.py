from django.db import models


class SyncDate(models.Model):
    datetime = models.DateTimeField("Дата синхронизации",
                                    auto_now=True,
                                    auto_now_add=False)

    class Meta(object):
        verbose_name = "дата синхронизации"
        verbose_name_plural = "даты синхронизации"

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
        verbose_name = "водитель"
        verbose_name_plural = "водители"

    def __str__(self):
        return self.name
