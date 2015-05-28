# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('aeroplanes', '0006_auto_20150528_1543'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='aeroplane',
            name='opening_airframe_hours_after_last_check',
        ),
    ]
