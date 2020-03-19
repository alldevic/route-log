from django.core.management.base import BaseCommand

from ...models import SyncDate


class Command(BaseCommand):
    help = 'Удаление локальных данных'

    def add_arguments(self, parser):
        parser.add_argument('--pk', type=int)

    # TODO: fix without param
    def handle(self, *args, **options):
        if (options.get("pk"), None):
            SyncDate.objects.get(pk=options["pk"]).delete()
        else:
            SyncDate.objects.all().delete()
