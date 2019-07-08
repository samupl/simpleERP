import datetime
import decimal
import re
from collections import namedtuple

from django.http import HttpResponse
from django.shortcuts import render

from apps.invoices.models import Invoice

InvoicePosition = namedtuple(
    'InvoicePosition',
    'invoice net gross pln_net pln_gross net_tax vat_tax currency_rate'
)

RATE_REGEXP = re.compile(r'Kurs waluty: (\d*,?\.?\d*) PLN/')
NETTO_TAX = decimal.Decimal('0.19')


quarters = {
    0: [1, 2, 3],
    1: [4, 5, 6],
    2: [7, 8, 9],
    3: [10, 11, 12],
}


def costs(request, year=None, quarter=None):
    now = datetime.datetime.now()

    if year is None:
        year = now.year

    if quarter is None:
        quarter = (now.month - 1) // 3

    months = quarters[int(quarter)]

    invoices = Invoice.objects.filter(
        date_issued__year=year,
        date_issued__month__in=months,
    ).exclude(
        invoice_pdf_file='',
    )

    invoice_positions = []
    for invoice in invoices:
        pln_net = invoice.money_net
        pln_gross = invoice.money_gross
        currency_rate = None

        currency_rate_match = RATE_REGEXP.search(invoice.comments)
        if currency_rate_match:
            currency_rate = decimal.Decimal(
                currency_rate_match.groups()[0].replace(',', '.')
            )

            pln_net *= currency_rate
            pln_gross *= currency_rate

        invoice_positions.append(
            InvoicePosition(
                invoice=invoice,
                net='{} {}'.format(
                    invoice.money_net, invoice.currency.code
                ),
                gross='{} {}'.format(
                    invoice.money_gross, invoice.currency.code
                ),
                pln_net=pln_net,
                pln_gross=pln_gross,
                currency_rate=currency_rate,
                net_tax=NETTO_TAX * pln_net,
                vat_tax=invoice.total_taxes,
            )
        )

    total_vat_tax = sum([ip.vat_tax for ip in invoice_positions])
    total_income_tax = sum([ip.net_tax for ip in invoice_positions])
    return render(
        request,
        'costs/costs.html',
        {
            'invoice_positions': invoice_positions,
            'total_vat_tax': total_vat_tax,
            'total_income_tax': total_income_tax,
        }
    )
