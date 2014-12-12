# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('lunch', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='event',
            name='vendor',
            field=models.ForeignKey(default=0, to='lunch.Vendor'),
            preserve_default=True,
        ),
    ]
