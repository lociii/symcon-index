# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2016-12-30 12:02
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('symcon', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='library',
            name='description',
            field=models.TextField(default='', verbose_name='Description'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='library',
            name='title',
            field=models.TextField(default='', verbose_name='Title'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='module',
            name='description',
            field=models.TextField(default='', verbose_name='Description'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='module',
            name='title',
            field=models.TextField(default='', verbose_name='Title'),
            preserve_default=False,
        ),
    ]
