# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('log', '0003_techlogentry_owner'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='techlogentry',
            name='date',
        ),
    ]
