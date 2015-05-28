# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('aeroplanes', '0004_remove_aeroplane_opening_ttaf'),
        ('log', '0004_remove_techlogentry_date'),
    ]

    operations = [
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
