# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('group', '0002_auto_20150607_2309'),
    ]

    operations = [
        migrations.AlterField(
            model_name='groupmemberprofile',
            name='role',
            field=models.CharField(max_length=200, null=True),
        ),
    ]
