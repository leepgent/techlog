# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('aeroplanes', '0004_auto_20150902_1316'),
    ]

    operations = [
        migrations.AlterField(
            model_name='aeroplane',
            name='opening_ttp',
            field=models.FloatField(),
        ),
    ]
