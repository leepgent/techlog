# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('group', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='GroupMemberProfile',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('role', models.CharField(max_length=200)),
                ('administrator', models.BooleanField()),
                ('current_rate_includes_fuel', models.BooleanField()),
                ('current_charge_regime', models.CharField(max_length=20, choices=[(b'tacho', b'Tacho'), (b'block2block', b'Block-to-block'), (b'hobbs', b'Hobbs'), (b'airborne', b'Airborne')])),
                ('current_cost_per_unit', models.FloatField()),
            ],
        ),
        migrations.RemoveField(
            model_name='groupprofile',
            name='administrators',
        ),
        migrations.AddField(
            model_name='groupprofile',
            name='current_fuel_rebate_price_per_litre',
            field=models.FloatField(default=1.584),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='groupmemberprofile',
            name='group',
            field=models.ForeignKey(to='group.GroupProfile'),
        ),
        migrations.AddField(
            model_name='groupmemberprofile',
            name='member',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL),
        ),
    ]
