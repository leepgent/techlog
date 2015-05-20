# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('aeroplanes', '0002_auto_20150520_2346'),
    ]

    operations = [
        migrations.CreateModel(
            name='TechLogEntry',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('date', models.DateField()),
                ('commander', models.TextField(max_length=100)),
                ('departure_location', models.TextField(max_length=100)),
                ('arrival_location', models.TextField(max_length=100)),
                ('departure_time', models.TimeField()),
                ('arrival_time', models.TimeField()),
                ('departure_tacho', models.FloatField()),
                ('arrival_tacho', models.FloatField()),
                ('fuel_uplift', models.FloatField()),
                ('oil_uplift', models.FloatField()),
                ('defects', models.TextField(max_length=200)),
                ('check_a_completed', models.BooleanField()),
                ('aeroplane', models.ForeignKey(to='aeroplanes.Aeroplane')),
            ],
        ),
    ]
