# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('group', '0003_auto_20150707_1550'),
    ]

    operations = [
        migrations.AddField(
            model_name='groupprofile',
            name='default_charge_regime',
            field=models.CharField(default=b'tacho', max_length=20, choices=[(b'tacho', b'Tacho'), (b'block2block', b'Block-to-block'), (b'hobbs', b'Hobbs'), (b'airborne', b'Airborne')]),
        ),
        migrations.AddField(
            model_name='groupprofile',
            name='default_cost_per_unit',
            field=models.FloatField(default=65),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='groupprofile',
            name='default_rate_includes_fuel',
            field=models.BooleanField(default=True),
            preserve_default=False,
        ),
    ]
