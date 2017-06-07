from django.contrib import admin
from django.utils.translation import ugettext_lazy as _

from apps.invoices.models import Invoice, InvoicePosition, InvoiceSeries


class InvoiceSeriesAdmin(admin.ModelAdmin):
    list_display = ['name', 'pattern', 'mode']


class InvoicePositionInline(admin.TabularInline):
    model = InvoicePosition
    extra = 1


class InvoiceAdmin(admin.ModelAdmin):
    list_display = ['invoice_number', 'issued_for', 'issued_by', 'date_issued', 'date_delivered', 'date_payment',
                    'money_net', 'money_gross', 'get_issued']
    search_fields = ['issued_for']
    readonly_fields = ['money_net', 'money_gross', 'issue_link', 'preview_link']
    inlines = [InvoicePositionInline]
    buttons = []

    def get_issued(self, obj):
        return obj.issued
    get_issued.boolean = True
    get_issued.short_description = _('Issued')

    def change_view(self, request, object_id, form_url='', extra_context=None):
        return super(InvoiceAdmin, self).change_view(request, object_id, form_url, extra_context)
    

class InvoicePositionAdmin(admin.ModelAdmin):
    list_display = ['invoice', 'description', 'count', 'money_net', 'tax', 'total_net', 'total_gross']
    readonly_fields = ['total_net', 'total_gross']


# Register models in admin site
admin.site.register(Invoice, InvoiceAdmin)
admin.site.register(InvoiceSeries, InvoiceSeriesAdmin)
admin.site.register(InvoicePosition, InvoicePositionAdmin)
