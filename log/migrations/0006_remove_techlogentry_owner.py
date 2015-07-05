# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('log', '0005_auto_20150607_2309'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='techlogentry',
            name='owner',
        ),
    ]
