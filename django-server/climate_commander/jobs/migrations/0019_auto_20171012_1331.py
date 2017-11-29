# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('jobs', '0018_auto_20160823_1611'),
    ]

    operations = [
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
    ]
