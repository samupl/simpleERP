from django.contrib import admin

from apps.ledger.models import LedgerEntry


class LedgerEntryAdmin(admin.ModelAdmin):
    list_display = ['date', 'company', 'buyer_name', 'description',
                    'income_total', 'cost_total']


# Register models in admin site
admin.site.register(LedgerEntry, LedgerEntryAdmin)
