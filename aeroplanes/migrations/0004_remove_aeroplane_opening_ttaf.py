# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('aeroplanes', '0003_aeroplane_opening_airframe_hours_after_last_check'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='aeroplane',
            name='opening_ttaf',
        ),
    ]
