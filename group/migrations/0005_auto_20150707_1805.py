# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('group', '0004_auto_20150707_1739'),
    ]

    operations = [
        migrations.AddField(
            model_name='groupmemberprofile',
            name='current_rate_includes_oil',
            field=models.BooleanField(default=True),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='groupprofile',
            name='current_oil_rebate_price_per_litre',
            field=models.FloatField(default=6.6),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='groupprofile',
            name='default_rate_includes_oil',
            field=models.BooleanField(default=True),
            preserve_default=False,
        ),
    ]
