from django.core.management.base import BaseCommand, CommandError
from phonechecker.models import Check


class Command(BaseCommand):
    help = 'Closes the specified poll for voting'

    def add_arguments(self, parser):
        parser.add_argument('categories', nargs='+', type=str)

    def handle(self, *args, **options):
        for cat in options['categories']:
            if cat.lower() == 'all':
                Check.objects.all().delete()
            if cat.lower() == 'pendings':
                Check.objects.filter(result=0).delete()
            if cat.lower() == 'processing':
                Check.objects.filter(result=4).delete()
