from django.core.management import BaseCommand

from apps.invoices.models import Invoice


class Command(BaseCommand):

    def add_arguments(self, parser):
        parser.add_argument('invoice_id', type=int)

    def handle(self, *args, **options):
        invoice = Invoice.objects.get(options['invoice_id'])
        invoice.render_pdf()

