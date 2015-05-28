# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('aeroplanes', '0005_auto_20150528_1510'),
    ]

    operations = [
        migrations.AlterField(
            model_name='aeroplane',
            name='last_annual',
            field=models.DateTimeField(),
        ),
    ]
