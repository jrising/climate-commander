# -*- coding: utf-8 -*-
# Generated by Django 1.9.8 on 2016-08-23 07:58
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('jobs', '0013_auto_20160823_0040'),
    ]

    operations = [
        migrations.AddField(
            model_name='job',
            name='running',
            field=models.BooleanField(default=False),
            preserve_default=False,
        ),
    ]
