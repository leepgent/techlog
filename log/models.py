from django.conf import settings
from django.db import models
from django.utils import timezone
from aeroplanes.models import Aeroplane

class Check(models.Model):
    aeroplane = models.ForeignKey(Aeroplane)
    time = models.DateTimeField()
    type = models.CharField(max_length=10, choices=Aeroplane.CHECK_TYPE_CHOICES)
    ttaf = models.FloatField()
    opening_hours_after_this_check = models.FloatField(default=0)

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
        since = self.aeroplane.check_set.filter(time__lte=self.departure_time).order_by("time").last()
        entries = self.aeroplane.techlogentry_set.filter(arrival_time__gte=since.time, arrival_time__lte=self.arrival_time)
        hours = reduce(lambda h, entry: h+entry.airborne_time, list(entries), timezone.timedelta(0))
        hours_in_decimal = hours.total_seconds() / (60*60)
        return since.ttaf + since.opening_hours_after_this_check + hours_in_decimal

    @property
    def until_next_check(self):
        #since = self.aeroplane.last_check

        since = self.aeroplane.check_set.filter(time__lte=self.departure_time).order_by("time").last()

        entries = self.aeroplane.techlogentry_set.filter(departure_time__gt=since.time).filter(arrival_time__lte=self.arrival_time)
        hours = reduce(lambda h, entry: h+entry.airborne_time, list(entries), timezone.timedelta(0))  #  Can't use Django Aggregate/Sum because time isn't stored in DB
        hours_in_decimal = hours.total_seconds() / (60*60)  # Like our stored DB 'hours' values, we need hours + decimal fraction of hours
        return Aeroplane.MAX_HOURS_BETWEEN_CHECKS - since.opening_hours_after_this_check - hours_in_decimal
