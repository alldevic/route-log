import datetime

import zeep
from django.core.management.base import BaseCommand
from requests import Session
from requests.auth import HTTPBasicAuth
from zeep.cache import InMemoryCache
from zeep.transports import Transport

from route_log_prj import settings as settings

from ...models import Device, Driver, GeoZone, Point, SyncDate, \
    FlatTableRow, FlatTable


class Command(BaseCommand):
    help = 'Загрузка данных с сервера навигации'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        session = Session()
        session.auth = HTTPBasicAuth(settings.NAV_USER, settings.NAV_PASS)

        self.client = zeep.Client(settings.NAV_HOST,
                                  transport=Transport(session=session,
                                                      cache=InMemoryCache()))

    def getAllDevices(self, sync_date):
        res = self.client.service.getAllDevices()
        for item in res:
            Device.objects.create(
                sync_date=sync_date,
                name=item.name,
                reg_number=item.regNumber,
                serial_number=item.serialNumber,
                garage_number=item.garageNumber,
                phone=item.phone,
                sim_number=item.simNumber,
                fuel_sort=item.fuelSort,
                brand=item.brand,
                description=item.description,
                group_ids=str(item.groupIds),
                nav_id=item.id,
            )

    def getAllDrivers(self, sync_date):
        res = self.client.service.getAllDrivers()
        for item in res:
            Driver.objects.create(
                sync_date=sync_date,
                fname=item.fname,
                mname=item.mname,
                lname=item.lname,
                licence_nr=item.licenceNr,
                phone=item.phone,
                category=item.category,
                internal_nr=item.internalNr,
                driver_cat=item.driverCat,
                nav_id=item.id,
            )

    def getAllGeoZones(self, sync_date):
        res = self.client.service.getAllGeoZones()
        self.stdout.write(self.style.SUCCESS(
            'getAllGeoZones - SOAP - SUCCESS'))
        for item in res:
            points = [
                Point.objects.create(
                    sync_date=sync_date,
                    lat=pt.lat,
                    lon=pt.lon) for pt in item.points
            ]
            tmp = GeoZone.objects.create(
                sync_date=sync_date,
                nav_id=item.id,
                name=item.name,
            )
            tmp.points.set(points)
            tmp.save()

    def getFlatTableSimple(self, sync_date, device_id, dt):
        dt0 = dt - datetime.timedelta(days=1)
        date_from = f"{dt0.year}-0{dt0.month}-{dt0.day}T16:00:00"
        date_to = f"{dt.year}-0{dt.month}-{dt.day}T16:59:59"

        res = self.client.service.getFlatTableSimple(device_id,
                                                     date_from, date_to,
                                                     10000, [0, ], ['Rw', ])
        self.stdout.write(self.style.SUCCESS(
            'getFlatTableSimple - SOAP - SUCCESS'))

        rows = [FlatTableRow.objects.create(
            sync_date=sync_date,
            utc=str(x.utc),
            values=str(x.values[0]['pointValue'])
        ) for x in res.rows]

        tmp = FlatTable.objects.create(
            sync_date=sync_date,
            ts=res.ts,
        )
        tmp.rows.set(rows)
        tmp.save()

    def add_arguments(self, parser):
        parser.add_argument('--entity', type=str)

    def handle(self, *args, **options):
        sync_date = SyncDate.objects.create()
        # if options['entity']:
        #     self.stdout.write(
        #         self.style.SUCCESS(f'Hello {options["entity"]}'))
        # else:
        #     # self.stdout.write(
        #     #     self.style.SUCCESS('Hello all!'))
        self.getAllDevices(sync_date)
        self.stdout.write(self.style.SUCCESS('getAllDevices - SUCCESS'))
        self.getAllDrivers(sync_date)
        self.stdout.write(self.style.SUCCESS('getAllDrivers - SUCCESS'))
        self.getAllGeoZones(sync_date)
        self.stdout.write(self.style.SUCCESS('getAllGeoZones - SUCCESS'))
        for device in Device.objects.filter(sync_date=sync_date):
            self.getFlatTableSimple(sync_date,
                                    device.nav_id,
                                    datetime.datetime.now())
            self.stdout.write(
                self.style.SUCCESS(
                    f'getFlatTableSimple - {device.nav_id} - SUCCESS'))
