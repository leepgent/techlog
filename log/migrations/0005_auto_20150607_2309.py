# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('log', '0004_auto_20150607_2049'),
    ]

    operations = [
        migrations.AddField(
            model_name='techlogentry',
            name='charge_regime',
            field=models.CharField(default='tacho', max_length=20, choices=[(b'tacho', b'Tacho'), (b'block2block', b'Block-to-block'), (b'hobbs', b'Hobbs'), (b'airborne', b'Airborne')]),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='techlogentry',
            name='cost_per_unit',
            field=models.FloatField(default=80),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='techlogentry',
            name='fuel_rebate_price_per_litre',
            field=models.FloatField(default=1.584),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='techlogentry',
            name='rate_includes_fuel',
            field=models.BooleanField(default=True),
            preserve_default=False,
        ),
    ]
