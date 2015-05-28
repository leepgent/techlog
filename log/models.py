from django.conf import settings
from django.db import models
from django.utils import timezone
from aeroplanes.models import Aeroplane
from group.models import GroupMemberProfile


class TechLogEntry(models.Model):
    owner = models.ForeignKey(settings.AUTH_USER_MODEL)
    aeroplane = models.ForeignKey(Aeroplane)
    commander = models.TextField(max_length=100)
    departure_location = models.TextField(max_length=100)
    arrival_location = models.TextField(max_length=100)
    departure_time = models.DateTimeField()
    arrival_time = models.DateTimeField()
    departure_tacho = models.FloatField()
    arrival_tacho = models.FloatField()
    fuel_uplift = models.FloatField()
    oil_uplift = models.FloatField()
    defects = models.TextField(max_length=200)
    check_a_completed = models.BooleanField()

    fuel_rebate_price_per_litre = models.FloatField()

    # engine duration, flight duration and airborne times dynamically calculated

    @property
    def engine_duration(self):
        return self.arrival_tacho - self.departure_tacho

    @property
    def flight_duration(self):
        return self.arrival_time - self.departure_time

    @property
    def airborne_time(self):
        return self.flight_duration - timezone.timedelta(minutes=10)

    @property
    def ttaf(self):
        entries = self.aeroplane.techlogentry_set.filter(arrival_time__lte=self.arrival_time)
        hours = reduce(lambda h, entry: h+entry.airborne_time, list(entries), timezone.timedelta(0))
        hours_in_decimal = hours.total_seconds() / (60*60)
        return self.aeroplane.last_check_ttaf + self.aeroplane.opening_airframe_hours_after_last_check + hours_in_decimal

    @property
    def until_next_check(self):
        since = self.aeroplane.last_check
        entries = self.aeroplane.techlogentry_set.filter(departure_time__gt=since).filter(arrival_time__lte=self.arrival_time)
        hours = reduce(lambda h, entry: h+entry.airborne_time, list(entries), timezone.timedelta(0))  #  Can't use Django Aggregate/Sum because time isn't stored in DB
        hours_in_decimal = hours.total_seconds() / (60*60)  # Like our stored DB 'hours' values, we need hours + decimal fraction of hours
        return Aeroplane.MAX_HOURS_BETWEEN_CHECKS - self.aeroplane.opening_airframe_hours_after_last_check - hours_in_decimal

    @property
    def cost(self):
        group = self.aeroplane.owning_group
        group_profile = group.groupprofile
        user = self.owner
        memberprofile = GroupMemberProfile.objects.get(group=group_profile, member=user)
        rate = memberprofile.cost_per_hour

        if memberprofile.charge_regime == GroupMemberProfile.CHARGE_REGIME_TACHO_HOURS:
            cost = self.engine_duration * rate
        else:
            cost = 0

        return cost
