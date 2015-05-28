# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('aeroplanes', '0004_remove_aeroplane_opening_ttaf'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='aeroplane',
            name='last_check',
        ),
        migrations.RemoveField(
            model_name='aeroplane',
            name='last_check_ttaf',
        ),
        migrations.RemoveField(
            model_name='aeroplane',
            name='last_check_type',
        ),
    ]
