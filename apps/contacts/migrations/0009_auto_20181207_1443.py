# -*- coding: utf-8 -*-
# Generated by Django 1.9.1 on 2018-12-07 14:43
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('contacts', '0008_auto_20181207_1436'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='companybankaccount',
            options={'verbose_name': 'Bank Account', 'verbose_name_plural': 'Bank Accounts'},
        ),
    ]