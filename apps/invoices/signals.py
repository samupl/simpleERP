from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver

from apps.invoices.models import InvoicePosition


@receiver(post_save, sender=InvoicePosition)
@receiver(post_delete, sender=InvoicePosition)
def invoice_position_changed(sender, instance, **kwargs):
    instance.invoice.recount_prices()
