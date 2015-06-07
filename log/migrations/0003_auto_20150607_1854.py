# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('log', '0002_techlogentry_consumables_receipt_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='techlogentry',
            name='consumables_receipt_image',
            field=models.ImageField(null=True, upload_to=b''),
        ),
    ]
