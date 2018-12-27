# -*- coding: utf-8 -*-
# Generated by Django 1.9.1 on 2018-12-27 08:29
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('invoices', '0016_tax_display'),
    ]

    operations = [
        migrations.AlterField(
            model_name='invoiceposition',
            name='tax',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='invoices.Tax'),
        ),
    ]