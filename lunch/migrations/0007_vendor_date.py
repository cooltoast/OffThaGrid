# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('lunch', '0006_auto_20141215_1120'),
    ]

    operations = [
        migrations.AddField(
            model_name='vendor',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2014, 12, 15, 0, 0), blank=True),
            preserve_default=True,
        ),
    ]
