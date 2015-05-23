# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('group', '0003_auto_20150523_2223'),
    ]

    operations = [
        migrations.AlterField(
            model_name='groupprofile',
            name='roles',
            field=models.ManyToManyField(to='group.GroupRole', blank=True),
        ),
    ]
