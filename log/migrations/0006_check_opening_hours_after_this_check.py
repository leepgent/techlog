# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('log', '0005_check'),
    ]

    operations = [
        migrations.AddField(
            model_name='check',
            name='opening_hours_after_this_check',
            field=models.FloatField(default=0),
        ),
    ]
