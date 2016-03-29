# -*- coding: utf-8 -*-
# Generated by Django 1.9.1 on 2016-03-29 19:19
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='LedgerEntry',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField(verbose_name='Date')),
                ('invoice_no', models.CharField(max_length=256, verbose_name='Invoice/Receipt number')),
                ('buyer_name', models.CharField(max_length=1024, verbose_name='Buyer name')),
                ('buyer_address', models.CharField(max_length=1024, verbose_name='Buyer address')),
                ('description', models.CharField(max_length=1024, verbose_name='Description')),
                ('income_sold', models.DecimalField(blank=True, decimal_places=2, default=0, max_digits=32, verbose_name='Income from sold goods and services')),
                ('income_other', models.DecimalField(blank=True, decimal_places=2, default=0, max_digits=32, verbose_name='Other income')),
                ('income_total', models.DecimalField(blank=True, decimal_places=2, default=0, max_digits=32, verbose_name='Total income')),
                ('materials_cost', models.DecimalField(blank=True, decimal_places=2, default=0, max_digits=32, verbose_name='The purchase of commercial goods and materials at purchase prices')),
                ('materials_incidental_cost', models.DecimalField(blank=True, decimal_places=2, default=0, max_digits=32, verbose_name='Incidental costs of purchase')),
                ('cost_salary', models.DecimalField(blank=True, decimal_places=2, default=0, max_digits=32, verbose_name='Remuneration in cash and in kind')),
                ('cost_other', models.DecimalField(blank=True, decimal_places=2, default=0, max_digits=32, verbose_name='Other costs')),
                ('cost_total', models.DecimalField(blank=True, decimal_places=2, default=0, max_digits=32, verbose_name='Remuneration in cash and in kind')),
                ('column_15', models.CharField(max_length=1024, verbose_name='Additional info (not required)')),
                ('comments', models.CharField(max_length=1024, verbose_name='Comments')),
            ],
        ),
    ]