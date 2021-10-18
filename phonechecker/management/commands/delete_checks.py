from django.core.management.base import BaseCommand, CommandError
from phonechecker.models import Check


class Command(BaseCommand):
    help = 'Closes the specified poll for voting'

    def add_arguments(self, parser):
        parser.add_argument('--categories', nargs='+', type=str)
        parser.add_argument('--source', type=str)

    def handle(self, *args, **options):
        categories = options.get('categories', [])
        if categories:
            for cat in categories:
                if cat.lower() == 'all':
                    Check.objects.all().delete()
                if cat.lower() == 'pendings':
                    Check.objects.filter(result=0).delete()
                if cat.lower() == 'processing':
                    Check.objects.filter(result=4).delete()

        if options['source']:
            Check.objects.filter(source__icontains=options['source']).delete()
