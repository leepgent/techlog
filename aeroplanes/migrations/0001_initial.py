# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0006_require_contenttypes_0002'),
    ]

    operations = [
        migrations.CreateModel(
            name='Aeroplane',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('registration', models.CharField(max_length=10)),
                ('registered', models.DateField()),
                ('manufacturer', models.CharField(max_length=200)),
                ('type', models.CharField(max_length=200)),
                ('model', models.CharField(max_length=200)),
                ('mtow', models.IntegerField()),
                ('built', models.IntegerField()),
                ('engine_count', models.IntegerField()),
                ('engine', models.CharField(max_length=100)),
                ('propeller', models.CharField(max_length=100)),
                ('last_annual', models.DateTimeField()),
                ('opening_tte', models.FloatField()),
                ('opening_time', models.FloatField()),
                ('arc_expiry', models.DateField()),
                ('insurance_expiry', models.DateField()),
                ('owning_group', models.ForeignKey(to='auth.Group')),
            ],
        ),
        migrations.CreateModel(
            name='Check',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('time', models.DateTimeField()),
                ('type', models.CharField(max_length=10, choices=[(b'50HOURS1', b'50 hours (first)'), (b'50HOURS2', b'50 hours (second)'), (b'150HOURS', b'150 hours'), (b'ANNUAL', b'Annual')])),
                ('ttaf', models.FloatField()),
                ('aeroplane', models.ForeignKey(to='aeroplanes.Aeroplane')),
            ],
        ),
    ]
