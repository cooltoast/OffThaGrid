# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('lunch', '0002_remove_event_location'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Event',
        ),
    ]
