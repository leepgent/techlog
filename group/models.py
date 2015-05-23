import uuid
from django.conf import settings
from django.contrib.auth.models import Group
from django.db import models


class GroupRole(models.Model):
    name = models.CharField(max_length=50)
    role = models.CharField(max_length=50)
    contact_info = models.CharField(max_length=100)


""" Group have aeroplanes (already done), administrators and a number of defined generic roles and static doc uploads.
They also have a secret key which will allow membership of the group.
We'll use a SlugField for URLS (and maybe the secret key, too)
"""
class GroupProfile(models.Model):
    group = models.OneToOneField(Group)
    administrators = models.ManyToManyField(settings.AUTH_USER_MODEL)
    roles = models.ManyToManyField(GroupRole, blank=True)
    secret_key = models.UUIDField(default=uuid.uuid4)
