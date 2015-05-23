# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('group', '0002_remove_groupprofile_slug'),
    ]

    operations = [
        migrations.AlterField(
            model_name='groupprofile',
            name='secret_key',
            field=models.UUIDField(default=uuid.uuid4),
        ),
    ]
