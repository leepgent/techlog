# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('aeroplanes', '0003_check_tte'),
    ]

    operations = [
        migrations.AddField(
            model_name='aeroplane',
            name='opening_ttp',
            field=models.FloatField(default=0),
        ),
        migrations.AddField(
            model_name='check',
            name='ttp',
            field=models.FloatField(default=0),
        ),
    ]
