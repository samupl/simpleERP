# -*- coding: utf-8 -*-
# Generated by Django 1.9.1 on 2018-12-27 08:45
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('invoices', '0017_auto_20181227_0829'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='tax',
            options={'verbose_name': 'Tax', 'verbose_name_plural': 'Taxes'},
        ),
        migrations.AddField(
            model_name='currency',
            name='name_dative',
            field=models.CharField(default='', max_length=128, verbose_name='Name 3'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='currency',
            name='name_denominator',
            field=models.CharField(default='', max_length=128, verbose_name='Name 2'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='currency',
            name='name_genitive',
            field=models.CharField(default='', max_length=128, verbose_name='Name 1'),
            preserve_default=False,
        ),
    ]
