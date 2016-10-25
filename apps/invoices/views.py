import os

import pdfkit
from django.conf import settings
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render

from apps.invoices.models import Invoice


pdfkit_options = {
    'margin-top': '0px',
    'margin-right': '0px',
    'margin-bottom': '0px',
    'margin-left': '0px',
    'encoding': "UTF-8",
}


def render_invoice(request, invoice_id):
    invoice = get_object_or_404(Invoice, pk=invoice_id)
    return render(request, 'invoices/invoice.html', {
        'invoice': invoice,
        'demo': True,
        'taxes': invoice.aggregated_taxes})


def render_invoice_pdf(request, invoice_id):
    invoice = get_object_or_404(Invoice, pk=invoice_id)
    pdf = pdfkit.from_string(
        invoice.rendered_html, False, options=pdfkit_options
    )
    response = HttpResponse(content=pdf, content_type='application/pdf')
    return response


def issue(request, invoice_id):
    invoice = get_object_or_404(Invoice, pk=invoice_id)
    file_name = invoice.generate_filename()
    pdfkit.from_string(
        invoice.rendered_html,
        os.path.join(settings.MEDIA_ROOT, file_name),
        options=pdfkit_options
    )
    invoice.invoice_pdf_file = file_name
    invoice.save()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
