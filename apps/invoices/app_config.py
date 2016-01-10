from django.apps import AppConfig
from django.utils.translation import ugettext_lazy as _


class InvoicesAppConfig(AppConfig):
    name = 'apps.invoices'
    verbose_name = _('Invoices')

    def ready(self):
        from . import signals
