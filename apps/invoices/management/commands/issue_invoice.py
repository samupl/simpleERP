from django.core.management import BaseCommand


class Command(BaseCommand):

    def add_arguments(self, parser):
        parser.add_argument('invoice_id', type=int)

    def handle(self, *args, **options):
        pass

