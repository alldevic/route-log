from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = 'Загрузка данных с сервера навигации'

    def add_arguments(self, parser):
        parser.add_argument('--entity', type=str)

    def handle(self, *args, **options):
        if options['entity']:
            self.stdout.write(
                self.style.SUCCESS(f'Hello {options["entity"]}'))
        else:
            self.stdout.write(
                self.style.SUCCESS('Hello all!'))
