from django.apps import AppConfig
from django.utils.translation import ugettext_lazy as _


class LedgerAppConfig(AppConfig):
    name = 'apps.ledger'
    verbose_name = _('Ledger')

    def ready(self):
        pass
        # from . import signals
