import zeep
from django.core.management.base import BaseCommand
from requests import Session
from requests.auth import HTTPBasicAuth
from zeep.cache import InMemoryCache
from zeep.transports import Transport

from route_log_prj import settings as settings

from ...models import Device, SyncDate


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
