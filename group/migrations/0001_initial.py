# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings
import uuid


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('auth', '0006_require_contenttypes_0002'),
    ]

    operations = [
        migrations.CreateModel(
            name='GroupProfile',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('secret_key', models.UUIDField(default=uuid.uuid4)),
                ('administrators', models.ManyToManyField(to=settings.AUTH_USER_MODEL)),
                ('group', models.OneToOneField(to='auth.Group')),
            ],
        ),
        migrations.CreateModel(
            name='GroupRole',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=50)),
                ('role', models.CharField(max_length=50)),
                ('contact_info', models.CharField(max_length=100)),
            ],
        ),
        migrations.AddField(
            model_name='groupprofile',
            name='roles',
            field=models.ManyToManyField(to='group.GroupRole', blank=True),
        ),
    ]
