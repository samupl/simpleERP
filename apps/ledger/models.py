# -*- coding: utf-8 -*-

from django.db import models
from django.utils.translation import ugettext_lazy as _

from apps.contacts.models import Company


class LedgerEntry(models.Model):
    company = models.ForeignKey(Company)

    date = models.DateField(_('Date'))
    invoice_no = models.CharField(_('Invoice/Receipt number'), max_length=256)

    buyer_name = models.CharField(_('Buyer name'), max_length=1024)
    buyer_address = models.CharField(_('Buyer address'), max_length=1024)

    description = models.CharField(_('Description'), max_length=1024)

    income_sold = models.DecimalField(
        _('Income from sold goods and services'),
        max_digits=32, decimal_places=2, blank=True, default=0
    )
    income_other = models.DecimalField(
        _('Other income'),
        max_digits=32, decimal_places=2, blank=True, default=0
    )
    income_total = models.DecimalField(
        _('Total income'),
        max_digits=32, decimal_places=2, blank=True, default=0,
        help_text=_(
            'If you leave this field blank, it will be filled '
            'in automatically.'
        )
    )

    materials_cost = models.DecimalField(
        _('The purchase of commercial goods and materials at purchase prices'),
        max_digits=32, decimal_places=2, blank=True, default=0
    )
    materials_incidental_cost = models.DecimalField(
        _('Incidental costs of purchase'),
        max_digits=32, decimal_places=2, blank=True, default=0
    )

    cost_salary = models.DecimalField(
        _('Remuneration in cash and in kind'),
        max_digits=32, decimal_places=2, blank=True, default=0
    )
    cost_other = models.DecimalField(
        _('Other costs'),
        max_digits=32, decimal_places=2, blank=True, default=0
    )
    cost_total = models.DecimalField(
        _('Remuneration in cash and in kind'),
        max_digits=32, decimal_places=2, blank=True, default=0,
        help_text=_(
            'If you leave this field blank, it will be filled '
            'in automatically.'
        )
    )

    column_15 = models.CharField(
        _('Additional info (not required)'),
        max_length=1024, null=True, blank=True
    )
    comments = models.CharField(
        _('Comments'),
        max_length=1024, null=True, blank=True
    )

    def __str__(self):
        return (
            'Ledger entry ({date}, income: {income}, costs: {costs})'
        ).format(
            date=self.date,
            costs=self.cost_total,
            income=self.income_total
        )

    def recount_totals(self):
        if not self.income_total:
            self.income_total = self.income_other + self.income_sold

        if not self.cost_total:
            self.costs_total = self.cost_salary + self.cost_other
