# -*- coding: utf-8 -*-
# Generated by Django 1.9.6 on 2016-05-09 17:57
from __future__ import unicode_literals

from django.contrib.auth import get_user_model
from django.db import migrations

from log.views import _commanderise_user


def _go(apps, schema):
    TechLogEntry = apps.get_model('log', 'TechLogEntry')
    Users = get_user_model()

    for u in Users.objects.all():
        u.first_name = u.first_name.capitalize()
        u.last_name = u.last_name.capitalize()
        u.save()

    for tle in TechLogEntry.objects.all():
        cmdr = tle.commander

        u = Users.objects.filter(last_name=cmdr)[0]
        new_cmdr = _commanderise_user(u)

        tle.commander = new_cmdr
        tle.save()


class Migration(migrations.Migration):

    dependencies = [
        ('log', '0009_auto_20160116_0100'),
    ]

    operations = [
        migrations.RunPython(_go, migrations.RunPython.noop)
    ]