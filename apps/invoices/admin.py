from django.contrib import admin
from django.utils.translation import ugettext_lazy as _

from apps.invoices.models import (
    Invoice,
    InvoicePosition,
    InvoiceSeries,
    Currency,
    Tax,
)


class InvoiceSeriesAdmin(admin.ModelAdmin):
    list_display = ['name', 'pattern', 'mode']


class InvoicePositionInline(admin.TabularInline):
    model = InvoicePosition
    extra = 1


def make_paid(modeladmin, request, queryset):
    queryset.update(paid=True)


make_paid.short_description = _("Mark as paid")


def make_unpaid(modeladmin, request, queryset):
    queryset.update(paid=False)


make_unpaid.short_description = _("Mark as unpaid")


class InvoiceAdmin(admin.ModelAdmin):
    list_display = [
        'invoice_number', 'issued_for', 'issued_by', 'date_issued',
        'date_delivered', 'date_payment', 'money_net', 'money_gross',
        'get_issued', 'paid',
    ]
    search_fields = [
        'issued_for__person_first_name', 'issued_for__person_last_name',
        'issued_for__company_name', 'issued_for__company_nip',
        'issued_for__company_regon', 'invoice_number',
    ]
    readonly_fields = [
        'money_net', 'money_gross', 'issue_link', 'preview_link', 'paid',
    ]
    list_filter = ['issued_for__company_name', 'paid']
    inlines = [InvoicePositionInline]
    buttons = []
    actions = [make_paid, make_unpaid]

    def get_issued(self, obj):
        return obj.issued
    get_issued.boolean = True
    get_issued.short_description = _('Issued')

    def change_view(self, request, object_id, form_url='', extra_context=None):
        return super(InvoiceAdmin, self).change_view(request, object_id, form_url, extra_context)


class InvoicePositionAdmin(admin.ModelAdmin):
    list_display = ['invoice', 'description', 'count', 'money_net', 'tax', 'total_net', 'total_gross']
    readonly_fields = ['total_net', 'total_gross']


class CurrencyAdmin(admin.ModelAdmin):
    list_display = ['code', 'name']


class TaxAdmin(admin.ModelAdmin):
    list_display = ['name', 'display', 'value']


# Register models in admin site
admin.site.register(Invoice, InvoiceAdmin)
admin.site.register(InvoiceSeries, InvoiceSeriesAdmin)
admin.site.register(InvoicePosition, InvoicePositionAdmin)
admin.site.register(Currency, CurrencyAdmin)
admin.site.register(Tax, TaxAdmin)
