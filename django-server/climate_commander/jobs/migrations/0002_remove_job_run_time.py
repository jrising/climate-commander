# -*- coding: utf-8 -*-
# Generated by Django 1.9.8 on 2016-08-19 05:35
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('jobs', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='job',
            name='run_time',
        ),
    ]
