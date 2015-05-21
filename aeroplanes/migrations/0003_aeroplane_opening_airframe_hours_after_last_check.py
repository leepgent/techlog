# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('aeroplanes', '0002_auto_20150520_2346'),
    ]

    operations = [
        migrations.AddField(
            model_name='aeroplane',
            name='opening_airframe_hours_after_last_check',
            field=models.FloatField(default=0),
            preserve_default=False,
        ),
    ]
