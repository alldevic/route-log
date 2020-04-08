import datetime

import zeep
from django.core.management.base import BaseCommand
from requests import Session
from requests.auth import HTTPBasicAuth
from zeep.cache import InMemoryCache
from zeep.transports import Transport

from route_log_prj import settings as settings

from ...models import (Device, Driver, GeoZone, Point, SyncDate,
                       FlatTableRow, FlatTable, NavMtId)

from ...BulkCreateManager import BulkCreateManager
from django.utils import timezone


class Command(BaseCommand):
    help = 'Загрузка данных с сервера навигации'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        session = Session()
        session.auth = HTTPBasicAuth(settings.NAV_USER, settings.NAV_PASS)

        self.client = zeep.Client(settings.NAV_HOST,
                                  transport=Transport(session=session,
                                                      cache=InMemoryCache()))

    def getAllDevices(self, sync_date, bulk_mgr):
        res = self.client.service.getAllDevices()
        for item in res:
            bulk_mgr.add(Device(
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
            ))
        bulk_mgr.done()

    def getAllDrivers(self, sync_date, bulk_mgr):
        res = self.client.service.getAllDrivers()
        for item in res:
            bulk_mgr.add(Driver(
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
            ))
        bulk_mgr.done()

    def getAllGeoZones(self, sync_date, bulk_mgr):
        res = self.client.service.getAllGeoZones()
        self.stdout.write(self.style.SUCCESS(
            'getAllGeoZones - SOAP - SUCCESS'))

        mt_ids = [x for x in NavMtId.objects.filter(sync_date=sync_date)]

        for item in res:
            x_points = [Point(sync_date=sync_date,
                              lat=x.lat,
                              lon=x.lon) for x in item.points]
            points = Point.objects.bulk_create(x_points)

            mt = None
            for x in mt_ids:
                if int(x.nav_id) == int(item.id):
                    mt = x
                    break

            if mt is not None:
                mt_id = mt.mt_id
            else:
                mt_id = None

            tmp = GeoZone.objects.create(
                sync_date=sync_date,
                nav_id=item.id,
                name=item.name,
                mt_id=mt_id
            )
            tmp.points.set(points)
            tmp.save()

    # TODO: refact
    def getFlatTableSimple(self, sync_date, device_id, dt, bulk_mgr):
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

        date_from = f"{dt0.year}-{dt0month_str}-{dt0day_str}T22:00:00"
        date_to = f"{dt.year}-{dtmonth_str}-{dtday_str}T20:59:59"

        res = self.client.service.getFlatTableSimple(device_id,
                                                     date_from, date_to,
                                                     10000, [0, ], ['Rw', ])
        if res.rows:
            dt_date_to = datetime.datetime.strptime(
                date_to, '%Y-%m-%dT%H:%M:%S')
            cu_date_to = res.rows[-1].utc.replace(tzinfo=None)
            while (cu_date_to - dt_date_to) > datetime.timedelta(seconds=20):
                rs = self.client.service \
                    .getFlatTableSimple(device_id, cu_date_to, date_to,
                                        10000, [0, ], ['Rw', ])
                if rs.rows:
                    res += rs.rows
                cu_date_to = res.rows[-1].utc

            self.stdout.write(self.style.SUCCESS(
                'getFlatTableSimple - SOAP - SUCCESS'))

            rows = []
            car_id = Device.objects.get(nav_id=device_id, sync_date=sync_date)
            for row in res.rows:
                point_value = Point.objects.create(
                    sync_date=sync_date,
                    lat=row.values[0]['pointValue'].lat,
                    lon=row.values[0]['pointValue'].lon)
                rows.append(FlatTableRow(
                    sync_date=sync_date,
                    device=car_id,
                    utc=str(row.utc),
                    point_value=point_value))

            rows = FlatTableRow.objects.bulk_create(rows)
            tmp = FlatTable.objects.create(
                sync_date=sync_date,
                ts=res.ts,
            )
            tmp.rows.set(rows)
            tmp.save()

    def updateNavMt(self, sync_date, bulk_mgr):
        res = NavMtId.objects.filter(sync_date=SyncDate.objects.first())

        for row in res:
            bulk_mgr.add(NavMtId(
                sync_date=sync_date,
                name=row.name,
                nav_id=row.nav_id,
                mt_id=row.mt_id
            ))

    def add_arguments(self, parser):
        parser.add_argument('--date', type=self.get_date,
                            default=timezone.now())
        parser.add_argument('--count', type=int, default=1)
        parser.add_argument('--force', action='store_true', default=False)

    def get_date(self, obj):
        obj += " 00:01:00+0000"
        return timezone.datetime.strptime(obj, "%d.%m.%Y %H:%M:%S%z")

    #  TODO: add custom periods, now 1 sync in 24 hours
    def handle(self, *args, **options):
        count = options['count']
        force = options['force']

        for co in range(0, count):
            date = (options['date'] or timezone.localtime()) - \
                timezone.timedelta(days=co)
            sync_date = SyncDate.objects \
                .filter(datetime__year=date.year,
                        datetime__month=date.month,
                        datetime__day=date.day).last() or \
                SyncDate.objects.last()

            now = timezone.localtime()

            if ((sync_date.datetime.year == date.year) and
                (sync_date.datetime.month == date.month) and
                    (sync_date.datetime.day == date.day)):
                if force:
                    sync_date.delete()
                else:
                    self.stdout.write(self.style.SUCCESS(
                        f'Current sync date: {sync_date}'))
                    self.stdout.write(self.style.SUCCESS(f'Now: {now}'))
                    self.stdout.write(self.style.SUCCESS('Sync already done!'))
                    continue

            bulk_mgr = BulkCreateManager(chunk_size=250)
            sync_date = SyncDate.objects.create(datetime=date)
            begin_time = timezone.now()
            self.stdout.write(self.style.SUCCESS(
                f'BEGIN ALL: {begin_time}'))
            self.updateNavMt(sync_date, bulk_mgr)
            self.stdout.write(self.style.SUCCESS('NavMt - SUCCESS'))
            self.getAllDevices(sync_date, bulk_mgr)
            self.stdout.write(self.style.SUCCESS('getAllDevices - SUCCESS'))
            self.getAllDrivers(sync_date, bulk_mgr)
            self.stdout.write(self.style.SUCCESS('getAllDrivers - SUCCESS'))
            self.getAllGeoZones(sync_date, bulk_mgr)
            self.stdout.write(self.style.SUCCESS('getAllGeoZones - SUCCESS'))
            devices = [x for x in Device.objects.filter(sync_date=sync_date)]
            for device in devices:
                self.getFlatTableSimple(sync_date,
                                        device.nav_id,
                                        timezone.now(), bulk_mgr)
                self.stdout.write(
                    self.style.SUCCESS(
                        f'getFlatTableSimple - {device.nav_id} - SUCCESS'))
            end_time = timezone.now()
            self.stdout.write(self.style.SUCCESS(f'END ALL: {end_time}'))
            self.stdout.write(self.style.SUCCESS(
                f'ESTIMATED: {end_time - begin_time}'))
