# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('jobs', '0018_auto_20160823_1611'),
    ]

    operations = [
        migrations.AlterField(
            model_name='job',
            name='running',
            field=models.NullBooleanField(),
        ),
    ]
