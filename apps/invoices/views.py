import os

import pdfkit
from django.conf import settings
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render

from apps.invoices.models import Invoice


def render_invoice(request, invoice_id):
    invoice = get_object_or_404(Invoice, pk=invoice_id)
    return render(request, 'invoices/invoice.html', {
        'invoice': invoice,
        'demo': True,
        'taxes': invoice.aggregated_taxes})


def render_invoice_pdf(request, invoice_id):
    invoice = get_object_or_404(Invoice, pk=invoice_id)
    pdf = pdfkit.from_string(invoice.rendered_html, False)
    response = HttpResponse(content=pdf, content_type='application/pdf')
    return response


def issue(request, invoice_id):
    invoice = get_object_or_404(Invoice, pk=invoice_id)
    file_name = invoice.generate_filename()
    pdfkit.from_string(invoice.rendered_html, os.path.join(settings.MEDIA_ROOT, file_name))
    invoice.invoice_pdf_file = file_name
    invoice.save()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
