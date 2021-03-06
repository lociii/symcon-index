# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2017-01-01 15:31
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('symcon', '0003_auto_20161230_1957'),
    ]

    operations = [
        migrations.AlterField(
            model_name='library',
            name='author',
            field=models.CharField(blank=True, max_length=200, verbose_name='Author'),
        ),
        migrations.AlterField(
            model_name='library',
            name='build',
            field=models.IntegerField(blank=True, null=True, verbose_name='Build'),
        ),
        migrations.AlterField(
            model_name='library',
            name='date',
            field=models.IntegerField(blank=True, null=True, verbose_name='Date'),
        ),
        migrations.AlterField(
            model_name='library',
            name='description',
            field=models.TextField(blank=True, verbose_name='Description'),
        ),
        migrations.AlterField(
            model_name='library',
            name='name',
            field=models.CharField(blank=True, max_length=200, verbose_name='Name'),
        ),
        migrations.AlterField(
            model_name='library',
            name='readme_html',
            field=models.TextField(blank=True, verbose_name='Readme HTML'),
        ),
        migrations.AlterField(
            model_name='library',
            name='readme_markdown',
            field=models.TextField(blank=True, verbose_name='Readme MarkDown'),
        ),
        migrations.AlterField(
            model_name='library',
            name='title',
            field=models.TextField(blank=True, verbose_name='Title'),
        ),
        migrations.AlterField(
            model_name='library',
            name='url',
            field=models.URLField(blank=True, verbose_name='URL'),
        ),
        migrations.AlterField(
            model_name='library',
            name='version',
            field=models.CharField(blank=True, max_length=50, verbose_name='Version'),
        ),
        migrations.AlterField(
            model_name='module',
            name='description',
            field=models.TextField(blank=True, verbose_name='Description'),
        ),
        migrations.AlterField(
            model_name='module',
            name='name',
            field=models.CharField(blank=True, max_length=200, verbose_name='Name'),
        ),
        migrations.AlterField(
            model_name='module',
            name='prefix',
            field=models.CharField(blank=True, max_length=200, verbose_name='Prefix'),
        ),
        migrations.AlterField(
            model_name='module',
            name='readme_html',
            field=models.TextField(blank=True, verbose_name='Readme HTML'),
        ),
        migrations.AlterField(
            model_name='module',
            name='readme_markdown',
            field=models.TextField(blank=True, verbose_name='Readme MarkDown'),
        ),
        migrations.AlterField(
            model_name='module',
            name='title',
            field=models.TextField(blank=True, verbose_name='Title'),
        ),
        migrations.AlterField(
            model_name='module',
            name='type',
            field=models.IntegerField(blank=True, choices=[(0, 'Core'), (1, 'I/O'), (2, 'Splitter'), (3, 'Device'), (4, 'Configurator')], null=True, verbose_name='Type'),
        ),
        migrations.AlterField(
            model_name='module',
            name='vendor',
            field=models.CharField(blank=True, max_length=200, verbose_name='Vendor'),
        ),
        migrations.AlterField(
            model_name='repository',
            name='last_update',
            field=models.DateTimeField(blank=True, null=True, verbose_name='Last update'),
        ),
    ]
