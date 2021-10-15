from django.core.management.base import BaseCommand, CommandError
from phonechecker.models import Check


class Command(BaseCommand):
    help = 'Closes the specified poll for voting'

    # def add_arguments(self, parser):
    #     parser.add_argument('poll_ids', nargs='+', type=int)

    def handle(self, *args, **options):
        Check.objects.filter(result=0).delete()
