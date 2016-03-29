from django.db.models.signals import pre_save
from django.dispatch import receiver

from apps.ledger.models import LedgerEntry


@receiver(pre_save, sender=LedgerEntry)
def invoice_position_changed(sender, instance, **kwargs):
    instance.recount_totals()
