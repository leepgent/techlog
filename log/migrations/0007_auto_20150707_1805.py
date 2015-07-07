# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('log', '0006_remove_techlogentry_owner'),
    ]

    operations = [
        migrations.AddField(
            model_name='techlogentry',
            name='oil_rebate_price_per_litre',
            field=models.FloatField(default=6.6),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='techlogentry',
            name='rate_includes_oil',
            field=models.BooleanField(default=True),
            preserve_default=False,
        ),
    ]
