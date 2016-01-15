# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations

from log.models import ConsumablesReceipt


def _move_image_to_file_model(apps, schema_editor):
    TechLogEntry = apps.get_model("log", "TechLogEntry")
    for log_entry in TechLogEntry.objects.all():
        old_image = log_entry.consumables_receipt_image
        new_image = ConsumablesReceipt(log_entry_id=log_entry.id, image=old_image)
        new_image.save()


class Migration(migrations.Migration):

    dependencies = [
        ('log', '0007_auto_20150707_1805'),
    ]

    operations = [
        migrations.CreateModel(
            name='ConsumablesReceipt',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('image', models.FileField(upload_to=b'')),
            ],
        ),
        migrations.AddField(
            model_name='consumablesreceipt',
            name='log_entry',
            field=models.ForeignKey(to='log.TechLogEntry'),
        ),
        migrations.RunPython(_move_image_to_file_model),
        migrations.RemoveField(
            model_name='techlogentry',
            name='consumables_receipt_image',
        ),
    ]
