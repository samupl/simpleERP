# -*- coding: utf-8 -*-
# Generated by Django 1.9.1 on 2018-12-27 08:46
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('invoices', '0018_auto_20181227_0845'),
    ]

    operations = [
        migrations.RenameField(
            model_name='currency',
            old_name='name_dative',
            new_name='fulls_name_dative',
        ),
        migrations.RenameField(
            model_name='currency',
            old_name='name_denominator',
            new_name='fulls_name_denominator',
        ),
        migrations.RenameField(
            model_name='currency',
            old_name='name_genitive',
            new_name='fulls_name_genitive',
        ),
    ]
