# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('log', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='techlogentry',
            name='arrival_time',
            field=models.DateTimeField(),
        ),
        migrations.AlterField(
            model_name='techlogentry',
            name='departure_time',
            field=models.DateTimeField(),
        ),
    ]
