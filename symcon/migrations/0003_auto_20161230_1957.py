# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2016-12-30 18:57
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('symcon', '0002_auto_20161230_1302'),
    ]

    operations = [
        migrations.AddField(
            model_name='library',
            name='readme_html',
            field=models.TextField(default='', verbose_name='Readme HTML'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='library',
            name='readme_markdown',
            field=models.TextField(default='', verbose_name='Readme MarkDown'),
            preserve_default=False,
        ),
    ]
