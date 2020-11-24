import os

import pdfkit
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.utils import translation

from apps.invoices.models import Invoice



def render_invoice(request, invoice_id):
    with translation.override('pl'):
        invoice = get_object_or_404(Invoice, pk=invoice_id)
        return render(request, 'invoices/invoice.html', {
            'invoice': invoice,
            'demo': True,
            'taxes': invoice.aggregated_taxes})


def render_invoice_pdf(request, invoice_id):
    with translation.override('pl'):
        invoice = get_object_or_404(Invoice, pk=invoice_id)
        pdf = pdfkit.from_string(
            invoice.rendered_html, False, options=Invoice.pdfkit_options
        )
        response = HttpResponse(content=pdf, content_type='application/pdf')
        return response


def issue(request, invoice_id):
    with translation.override('pl'):
        invoice = get_object_or_404(Invoice, pk=invoice_id)
        invoice.render_pdf()
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
