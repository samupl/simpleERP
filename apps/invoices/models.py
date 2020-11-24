import datetime
import decimal
import os

import django.utils.timezone
import pdfkit
import requests
from django.conf import settings
from django.core.exceptions import ValidationError
from django.core.urlresolvers import reverse
from django.db import models
from django.db.models import F, Max
from django.template.loader import render_to_string
from django.utils import timezone
from django.utils import translation
from django.utils.safestring import mark_safe
from django.utils.translation import ugettext_lazy as _

from apps.contacts.models import Company, CompanyBankAccount, Contact


class Currency(models.Model):
    code = models.CharField(
        _('Code'),
        unique=True, max_length=16
    )
    name = models.CharField(
        _('Name'),
        max_length=128,
    )
    fulls_name_genitive = models.CharField(  # Dopełniacz
        _('Fulls name (genitive)'),
        max_length=128,
    )
    fulls_name_denominator = models.CharField(  # Mianownik
        _('Fulls name (denominator)'),
        max_length=128,
    )
    fulls_name_dative = models.CharField(  # Celownik
        _('Fulls name (dative)'),
        max_length=128,
    )
    halves_name_genitive = models.CharField(  # Dopełniacz
        _('Halves name (genitive)'),
        max_length=128,
    )
    halves_name_denominator = models.CharField(  # Mianownik
        _('Halves name (denominator)'),
        max_length=128,
    )
    halves_name_dative = models.CharField(  # Celownik
        _('Halves name (dative)'),
        max_length=128,
    )
    fetch_exchange_rate = models.BooleanField(
        _('Fetch average exchange rate'),
        default=False,
    )

    class Meta:
        verbose_name = _('Currency')
        verbose_name_plural = _('Currencies')

    def __str__(self):
        return '{} - {}'.format(self.code, self.name)

    def say_unit_fulls(self):
        return (
            self.fulls_name_genitive,
            self.fulls_name_denominator,
            self.fulls_name_dative,
        )

    def say_unit_halves(self):
        return (
            self.halves_name_genitive,
            self.halves_name_denominator,
            self.halves_name_dative,
        )

    def get_exchange_comment(self):
        if not self.fetch_exchange_rate:
            return ''

        now = timezone.now() - datetime.timedelta(days=1)
        while now.weekday() not in [0, 1, 2, 3, 4]:
            now = now - datetime.timedelta(days=1)

        effective_date = now.strftime('%Y-%m-%d')
        response = requests.get(
            (
                'http://api.nbp.pl/api/exchangerates/tables/A/{}?format=json'
            ).format(
                effective_date
            )
        )

        data = response.json()[0]
        rate = [rate for rate in data['rates'] if rate['code'] == self.code]
        rate = rate[0]['mid']
        return (
            'Kurs waluty: {rate} PLN/{code}; Tabela kursów średnich NBP nr '
            '{table_no} z dnia {date}'
        ).format(
            rate=rate,
            code=self.code,
            table_no=data['no'],
            date=data['effectiveDate'],
        )


class Tax(models.Model):
    name = models.CharField(
        _('Name'),
        max_length=128
    )
    display = models.CharField(
        _('Display'),
        max_length=128
    )
    value = models.DecimalField(
        _('Value'),
        max_digits=10,
        decimal_places=4,
        blank=True,
    )

    class Meta:
        verbose_name = _('Tax')
        verbose_name_plural = _('Taxes')

    def __str__(self):
        return self.name


class InvoiceSeries(models.Model):
    MODE_MONTHLY = 0
    MODE_YEARLY = 1

    MODES = {
        MODE_MONTHLY: _('Numbered monthly'),
        MODE_YEARLY: _('Numbered yearly')
    }

    name = models.CharField(_('Series name'), max_length=128)
    pattern = models.CharField(_('Series pattern'), max_length=128)
    mode = models.IntegerField(_('Mode'), choices=list(MODES.items()))

    def __str__(self):
        return self.name

    def generate_internal_number(self, date):
        qs = Invoice.objects.filter(series=self)

        # Filter based on the mode
        if self.mode == self.MODE_MONTHLY:
            qs = qs.filter(date_issued__month=date.month)
        elif self.mode == self.MODE_YEARLY:
            qs = qs.filter(date_issued__year=date.year)

        qs = qs.aggregate(Max('number'))
        number = qs['number__max']
        if number is None:
            number = 0

        return number + 1

    def generate_number(self, date, number):
        return self.pattern.format(
            month=date.month,
            year=date.year,
            day=date.day,
            number=number
        )

    class Meta:
        verbose_name = _('Invoice series')
        verbose_name_plural = _('Invoice series')


class Invoice(models.Model):

    pdfkit_options = {
        'margin-top': '10mm',
        'margin-right': '10mm',
        'margin-bottom': '10mm',
        'margin-left': '10mm',
        'page-height': '297mm',
        'page-width': '212mm',
        'encoding': "UTF-8",
        'dpi': '300',
    }

    # Defined at the top, because one of the fields uses this method
    def generate_filename(self, *_):
        series_prefix = self.series.pattern.split('/')[0]
        if not series_prefix:
            return 'invoice_{}.pdf'.format(self.pk)

        filename = '{series_prefix}_{month:>02}_{year}__{number}.pdf'.format(
            series_prefix=series_prefix,
            month=self.date_issued.month,
            year=self.date_issued.year,
            number=self.number,
        )
        return filename

    TYPE_INVOICE = 'invoice'
    TYPE_INVOICE_INSTALMENT = 'invoice-instalment'
    TYPE_INVOICE_FINAL = 'invoice-final'
    TYPE_PROFORMA = 'invoice-proforma'

    TYPES = {
        TYPE_INVOICE: _('VAT Invoice'),
        TYPE_INVOICE_INSTALMENT: _('Instalment invoice'),
        TYPE_INVOICE_FINAL: _('Final invoice'),
        TYPE_PROFORMA: _('Request for payment'),
    }

    PAYMENT_DATE_DEFAULT_DAYS = 14
    PAYMENT_BANK_TRANSFER = 0
    PAYMENT_PAYPAL = 1

    PAYMENTS = {
        PAYMENT_BANK_TRANSFER: _('Bank transfer'),
        PAYMENT_PAYPAL: _('PayPal'),
    }

    series = models.ForeignKey(InvoiceSeries, null=True, blank=True)
    invoice_type = models.CharField(
        _('Invoice type'), max_length=64, choices=list(TYPES.items())
    )
    number = models.IntegerField(
        _('Invoice internal number'), blank=True,
        help_text=_(
            'If you leave this field blank, it will be filled in '
            'automatically.'
        )
    )
    invoice_number = models.CharField(
        _('Invoice number'), max_length=128, blank=True,
        help_text=_(
            'If you leave this field blank, it will be filled in '
            'automatically.'
        )
    )

    issued_by = models.ForeignKey(Company)
    issued_for = models.ForeignKey(Contact)
    bank_account = models.ForeignKey(CompanyBankAccount, null=True)

    date_issued = models.DateField(
        _('Issue date'),
        default=django.utils.timezone.now
    )
    date_delivered = models.DateField(
        _('Delivery date'),
        default=django.utils.timezone.now
    )
    date_payment = models.DateField(
        _('Payment date'), null=True, blank=True,
        help_text=_(
            'If you leave this field blank, it will be filled in '
            'automatically.'
        )
    )

    money_net = models.DecimalField(
        _('Price net'), default=0, max_digits=32, decimal_places=2, blank=True,
        help_text=_(
            'The price will change automatically when you change an invoice '
            'position'
        )
    )
    money_gross = models.DecimalField(
        _('Price gross'), default=0, max_digits=32, decimal_places=2,
        blank=True, help_text=_(
            'The price will change automatically when you change an invoice '
            'position'
        )
    )
    currency = models.ForeignKey(Currency, null=True)
    comments = models.TextField(null=True, blank=True)
    payment_method = models.IntegerField(
        _('Payment method'),
        default=PAYMENT_BANK_TRANSFER,
        choices=list(PAYMENTS.items())
    )
    invoice_pdf_file = models.FileField(
        _('Invoice'), null=True, blank=True,
        upload_to=generate_filename
    )
    paid = models.BooleanField(_('Paid'), default=False)

    def save(self, *args, **kwargs):
        if not self.date_payment:
            self.date_payment = self.date_issued + datetime.timedelta(
                days=self.PAYMENT_DATE_DEFAULT_DAYS)

        if not self.number:
            self.number = self.series.generate_internal_number(
                date=self.date_issued)

        if not self.invoice_number:
            self.invoice_number = self.series.generate_number(
                date=self.date_issued, number=self.number)

        if not self.comments:
            self.comments = self.currency.get_exchange_comment()

        super().save(*args, **kwargs)

    def recount_prices(self):
        self.money_net = 0
        self.money_gross = 0
        for position in self.invoiceposition_set.all():
            self.money_net += position.total_net
            self.money_gross += position.total_gross
        self.save()

    @property
    def rendered_html(self):
        return render_to_string('invoices/invoice.html', {
            'invoice': self,
            'taxes': self.aggregated_taxes
        })

    @property
    def aggregated_taxes(self):
        positions = self.invoiceposition_set.all()
        taxes = {}
        for position in positions:
            tax = taxes.setdefault(
                position.tax.display,
                {
                    'total_net': decimal.Decimal(0),
                    'total_gross': decimal.Decimal(0),
                    'vat': decimal.Decimal(0),
                }
            )
            tax['total_net'] += position.total_net
            tax['total_gross'] += position.total_gross
            tax['vat'] += position.total_net * position.tax.value
        ret = {}
        for tax, t in taxes.items():
            ret[tax] = {
                'vat': t.get('vat').quantize(decimal.Decimal('0.01')),
                'total_net': t.get('total_net'),
                'total_gross': t.get('total_gross'),
            }
        return ret

    @property
    def total_taxes(self):
        taxes = self.invoiceposition_set.values('tax__display').annotate(
                vat=(F('total_net') * F('tax__value')))
        return sum([tax['vat'] for tax in taxes])

    @property
    def issued(self):
        return bool(self.invoice_pdf_file)

    @property
    def issue_link(self):
        if not self.pk:
            return ''

        if self.issued:
            return _('Invoice already issued')
        return mark_safe(
            _('<a href="{}">Issue this invoice</a>').format(
                reverse('invoices:issue', args=[self.pk])
            )
        )

    issue_link.fget.short_description = _('Issue')

    @property
    def preview_link(self):
        if not self.pk:
            return ''

        if self.issued:
            return _('Invoice already issued')
        return mark_safe(
            _('<a href="{}" target="_blank">Preview invoice</a>').format(
                reverse('invoices:render_invoice', args=[self.pk])
            )
        )

    preview_link.fget.short_description = _('Preview')

    @property
    def payment_method_verbose(self):
        return self.PAYMENTS[self.payment_method]

    @property
    def invoice_name(self):
        return self.TYPES[self.invoice_type]

    def __str__(self):
        return self.invoice_number

    def render_pdf(self):
        with translation.override('pl'):
            file_name = self.generate_filename()
            pdfkit.from_string(
                self.rendered_html,
                os.path.join(settings.MEDIA_ROOT, file_name),
                options=self.pdfkit_options
            )
            self.invoice_pdf_file = file_name
            self.save()

    class Meta:
        verbose_name = _('Invoice')
        verbose_name_plural = _('Invoices')


class InvoicePosition(models.Model):
    invoice = models.ForeignKey(
        Invoice,
        limit_choices_to={'invoice_pdf_file': ''}
    )
    description = models.CharField(_('Description'), max_length=256)
    money_net = models.DecimalField(_('Price net'), max_digits=32,
                                    decimal_places=2)
    total_net = models.DecimalField(_('Total net'), max_digits=32,
                                    decimal_places=2, blank=True, default=0)
    total_gross = models.DecimalField(_('Total gross'), max_digits=32,
                                      decimal_places=2, blank=True, default=0)

    tax = models.ForeignKey(Tax)
    count = models.IntegerField(_('Count'), default=1)

    def clean(self):
        if self.invoice.issued:
            raise ValidationError(_(
                'This invoice is already issued, you cannot modify its '
                'positions now.'
            ))

    def save(self, *args, **kwargs):
        self.total_net = self.money_net * self.count
        self.total_gross = self.total_net + (self.total_net * self.tax.value)
        super().save(*args, **kwargs)

    def __str__(self):
        return ''

    class Meta:
        verbose_name = _('Invoice position')
        verbose_name_plural = _('Invoice positions')
