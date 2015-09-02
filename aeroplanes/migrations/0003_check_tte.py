# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('aeroplanes', '0002_aeroplane_radio_expiry'),
    ]

    operations = [
        migrations.AddField(
            model_name='check',
            name='tte',
            field=models.FloatField(default=0),
        ),
    ]
