# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('lunch', '0003_delete_event'),
    ]

    operations = [
        migrations.AddField(
            model_name='vendor',
            name='date',
            field=models.DateTimeField(default=datetime.datetime.now, blank=True),
            preserve_default=True,
        ),
    ]
