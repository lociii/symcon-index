# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2017-01-03 20:04
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('symcon', '0006_auto_20170103_0001'),
    ]

    operations = [
        migrations.RenameField(
            model_name='librarybranch',
            old_name='min_version',
            new_name='req_ips_version',
        ),
    ]