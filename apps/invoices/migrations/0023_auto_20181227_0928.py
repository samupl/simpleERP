# -*- coding: utf-8 -*-
# Generated by Django 1.9.1 on 2018-12-27 09:28
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('invoices', '0022_invoice_comments'),
    ]

    operations = [
        migrations.AddField(
            model_name='currency',
            name='exchange_rate_url',
            field=models.CharField(blank=True, max_length=512, null=True, verbose_name='Exchange rate API URL'),
        ),
        migrations.AddField(
            model_name='currency',
            name='fetch_exchange_rate',
            field=models.BooleanField(default=False, verbose_name='Fetch average exchange rate'),
        ),
    ]
