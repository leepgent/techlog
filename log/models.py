from django.db import models
from django.utils import timezone
from aeroplanes.models import Aeroplane


class TechLogEntry(models.Model):
    aeroplane = models.ForeignKey(Aeroplane)
    date = models.DateField()
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
        entries = self.aeroplane.techlogentry_set.filter(arrival_time__lte=self.arrival_time)
        hours = reduce(lambda h, entry: h+entry.airborne_time, list(entries), timezone.timedelta(0))
        hours_in_decimal = hours.total_seconds() / (60*60)
        return self.aeroplane.last_check_ttaf + self.aeroplane.opening_airframe_hours_after_last_check + hours_in_decimal

    @property
    def until_next_check(self):
        since = self.aeroplane.last_check
        entries = self.aeroplane.techlogentry_set.filter(date__gt=since).filter(arrival_time__lte=self.arrival_time)
        hours = reduce(lambda h, entry: h+entry.airborne_time, list(entries), timezone.timedelta(0))  #  Can't use Django Aggregate/Sum because time isn't stored in DB
        hours_in_decimal = hours.total_seconds() / (60*60)  # Like our stored DB 'hours' values, we need hours + decimal fraction of hours
        return Aeroplane.MAX_HOURS_BETWEEN_CHECKS - self.aeroplane.opening_airframe_hours_after_last_check - hours_in_decimal
