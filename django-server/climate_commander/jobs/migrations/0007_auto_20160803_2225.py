# -*- coding: utf-8 -*-
# Generated by Django 1.9.8 on 2016-08-04 05:25
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('jobs', '0006_auto_20160803_2155'),
    ]

    operations = [
        migrations.AddField(
            model_name='server',
            name='crdntl_domain',
            field=models.CharField(default='haha', max_length=50),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='server',
            name='crdntl_password',
            field=models.CharField(default='yooo', max_length=20),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='server',
            name='crdntl_user',
            field=models.CharField(default='doh', max_length=50),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='server',
            name='roots_data',
            field=models.CharField(default='yeah', max_length=50),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='server',
            name='roots_src',
            field=models.CharField(default='kinda stupid', max_length=50),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='server',
            name='server_cpus',
            field=models.IntegerField(default=24),
            preserve_default=False,
        ),
    ]