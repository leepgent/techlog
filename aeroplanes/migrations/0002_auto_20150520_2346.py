# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('aeroplanes', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='aeroplane',
            name='last_check_ttaf',
            field=models.FloatField(default=2623),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='aeroplane',
            name='opening_ttaf',
            field=models.FloatField(default=0),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='aeroplane',
            name='opening_tte',
            field=models.FloatField(default=0),
            preserve_default=False,
        ),
    ]
