from django.core.management.base import BaseCommand

from ...models import Device, Driver, GeoZone, Point, SyncDate, \
    FlatTableRow, FlatTable


class Command(BaseCommand):
    help = 'Удаление локальных данных'

    def handle(self, *args, **options):
        SyncDate.objects.all().delete()
