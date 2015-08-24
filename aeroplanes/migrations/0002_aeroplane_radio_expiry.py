# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('aeroplanes', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='aeroplane',
            name='radio_expiry',
            field=models.DateField(default=datetime.datetime(2015, 8, 24, 16, 20, 38, 426000, tzinfo=utc)),
            preserve_default=False,
        ),
    ]
