# -*- coding: utf-8 -*-
# Generated by Django 1.9.8 on 2016-09-15 22:06
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('jobs', '0019_auto_20160824_1516'),
    ]

    operations = [
        migrations.AddField(
            model_name='server',
            name='crdntl_instanceip',
            field=models.GenericIPAddressField(null=True),
        ),
        migrations.AddField(
            model_name='server',
            name='crdntl_loginnode',
            field=models.CharField(max_length=20, null=True),
        ),
        migrations.AlterField(
            model_name='server',
            name='crdntl_domain',
            field=models.CharField(max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='server',
            name='crdntl_password',
            field=models.CharField(max_length=20, null=True),
        ),
        migrations.AlterField(
            model_name='server',
            name='crdntl_user',
            field=models.CharField(max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='server',
            name='server_cpus',
            field=models.IntegerField(null=True),
        ),
    ]
