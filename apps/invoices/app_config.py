from django.apps import AppConfig
from django.utils.translation import ugettext_lazy as _


DEFAULT_TAXES = [
    {
        'name': '23%',
        'display': '23 %',
        'value': '0.23',
    },
    {
        'name': 'Zwolniony',
        'display': 'zw',
        'value': '0',
    },
    {
        'name': 'Nie podlega',
        'display': 'np',
        'value': '0',
    },
]


class InvoicesAppConfig(AppConfig):
    name = 'apps.invoices'
    verbose_name = _('Invoices')

    def ready(self):
        from . import signals
        from apps.invoices.models import Tax
        # for tax_dict in DEFAULT_TAXES:
        #     Tax.objects.get_or_create(
        #         name=tax_dict['name'],
        #         defaults={
        #             'display': tax_dict['display'],
        #             'value': tax_dict['value'],
        #         }
        #     )
