import datetime

import zeep
from django.core.management.base import BaseCommand
from requests import Session
from requests.auth import HTTPBasicAuth
from zeep.cache import InMemoryCache
from zeep.transports import Transport

from route_log_prj import settings as settings

from ...models import Device, Driver, GeoZone, Point, SyncDate, \
    FlatTableRow, FlatTable, NavMtId


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

    # TODO: refact
    def getFlatTableSimple(self, sync_date, device_id, dt):
        dt0 = dt - datetime.timedelta(days=1)
        dt0month_str = dt0.month
        if dt0.month < 10:
            dt0month_str = '0' + str(dt0month_str)

        dt0day_str = dt0.day
        if dt0.day < 10:
            dt0day_str = '0' + str(dt0day_str)

        dtmonth_str = dt.month
        if dt.month < 10:
            dtmonth_str = '0' + str(dtmonth_str)

        dtday_str = dt.day
        if dt.day < 10:
            dtday_str = '0' + str(dtday_str)

        date_from = f"{dt0.year}-{dt0month_str}-{dt0day_str}T16:00:00"
        date_to = f"{dt.year}-{dtmonth_str}-{dtday_str}T16:59:59"

        res = self.client.service.getFlatTableSimple(device_id,
                                                     date_from, date_to,
                                                     10000, [0, ], ['Rw', ])
        self.stdout.write(self.style.SUCCESS(
            'getFlatTableSimple - SOAP - SUCCESS'))

        rows = []
        for row in res.rows:
            point_value = Point.objects.create(
                sync_date=sync_date,
                lat=row.values[0]['pointValue'].lat,
                lon=row.values[0]['pointValue'].lon)
            tmp = FlatTableRow.objects.create(
                sync_date=sync_date,
                utc=str(row.utc),
                point_value=point_value)
            rows.append(tmp)

        tmp = FlatTable.objects.create(
            sync_date=sync_date,
            ts=res.ts,
        )
        tmp.rows.set(rows)
        tmp.save()

    def updateNavMt(self, sync_date):
        res = NavMtId.objects.filter(sync_date=SyncDate.objects.first())
        for row in res:
            NavMtId.objects.create(
                sync_date=sync_date,
                name=row.name,
                nav_id=row.nav_id,
                mt_id=row.mt_id
            )

    def add_arguments(self, parser):
        parser.add_argument('--entity', type=str)

    #  TODO: add custom periods, now 1 sync in 24 hours
    def handle(self, *args, **options):
        sync_date = SyncDate.objects.last()

        if sync_date is None or \
           sync_date.datetime.year != datetime.datetime.now().year or \
           sync_date.datetime.month != datetime.datetime.now().month or \
           sync_date.datetime.day != datetime.datetime.now().day:
            sync_date = SyncDate.objects.create()
            self.stdout.write(self.style.SUCCESS('BEGIN ALL'))
            self.updateNavMt(sync_date)
            self.stdout.write(self.style.SUCCESS('NavMt - SUCCESS'))
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
            self.stdout.write(self.style.SUCCESS('END ALL'))
        else:
            self.stdout.write(self.style.SUCCESS('Sync already done!'))
