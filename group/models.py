import uuid
from django.conf import settings
from django.contrib.auth.models import Group
from django.db import models


class GroupRole(models.Model):
    name = models.CharField(max_length=50)
    role = models.CharField(max_length=50)
    contact_info = models.CharField(max_length=100)

    def __unicode__(self):
        return "{0} ({1})".format(self.name, self.role)


""" Group have aeroplanes (already done), administrators and a number of defined generic roles and static doc uploads.
They also have a secret key which will allow membership of the group.
We'll use a SlugField for URLS (and maybe the secret key, too)
"""
class GroupProfile(models.Model):
    group = models.OneToOneField(Group)
    roles = models.ManyToManyField(GroupRole, blank=True)
    current_fuel_rebate_price_per_litre = models.FloatField()
    secret_key = models.UUIDField(default=uuid.uuid4)

    def __unicode__(self):
        return "Profile for {0}".format(self.group.name)

class GroupMemberProfile(models.Model):
    CHARGE_REGIME_TACHO_HOURS = "tacho"
    CHARGE_REGIME_BLOCK_HOURS = "block2block"
    CHARGE_REGIME_HOBBS_HOURS = "hobbs"
    CHARGE_REGIME_AIRBORNE_HOURS = "airborne"

    CHARGE_REGIME_CHOICES = (
        (CHARGE_REGIME_TACHO_HOURS, "Tacho"),
        (CHARGE_REGIME_BLOCK_HOURS, "Block-to-block"),
        (CHARGE_REGIME_HOBBS_HOURS, "Hobbs"),
        (CHARGE_REGIME_AIRBORNE_HOURS, "Airborne"),
    )

    group = models.ForeignKey(GroupProfile)
    member = models.ForeignKey(settings.AUTH_USER_MODEL)
    role = models.CharField(max_length=200)
    administrator = models.BooleanField()

    current_rate_includes_fuel = models.BooleanField()
    current_charge_regime = models.CharField(max_length=20, choices=CHARGE_REGIME_CHOICES)
    current_cost_per_unit = models.FloatField()

    def __unicode__(self):
        return "{0} - {1}".format(self.group.group.name, self.member.get_username())
