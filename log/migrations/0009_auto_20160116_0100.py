# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


def _trash_empty_receipts(apps, schema_editor):
    ConsumablesReceipt = apps.get_model("log", "ConsumablesReceipt")
    ConsumablesReceipt.objects.filter(log_entry__fuel_uplift=0).delete()
    ConsumablesReceipt.objects.filter(log_entry__fuel_uplift__gt=0).filter(image='').delete()


class Migration(migrations.Migration):

    dependencies = [
        ('log', '0008_auto_20151206_2323'),
    ]

    operations = [
        migrations.RunPython(_trash_empty_receipts)
    ]
