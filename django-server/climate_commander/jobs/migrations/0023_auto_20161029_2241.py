# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('jobs', '0022_merge'),
    ]

    operations = [
        migrations.AddField(
            model_name='server',
            name='crdntl_instanceName',
            field=models.CharField(max_length=50, null=True),
        ),
        migrations.AddField(
            model_name='server',
            name='crdntl_pem',
            field=models.CharField(max_length=100, null=True),
        ),
    ]
