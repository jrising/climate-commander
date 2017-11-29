# -*- coding: utf-8 -*-
# Generated by Django 1.9.8 on 2016-08-19 06:15
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('jobs', '0003_job_run_time'),
    ]

    operations = [
        migrations.AlterField(
            model_name='job',
            name='pid',
            field=models.CharField(max_length=2000, null=True),
        ),
        migrations.AlterField(
            model_name='job',
            name='run_time',
            field=models.DateTimeField(null=True, verbose_name='Time of the Last Run'),
        ),
        migrations.AlterField(
            model_name='job',
            name='status',
            field=models.CharField(max_length=6000, null=True),
        ),
    ]
