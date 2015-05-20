from dateutil.relativedelta import relativedelta
from django.db import models
from aeroplanes.models import Aeroplane


class TechLogEntry(models.Model):
    aeroplane = models.ForeignKey(Aeroplane)
    date = models.DateField()
    commander = models.TextField(max_length=100)
    departure_location = models.TextField(max_length=100)
    arrival_location =  models.TextField(max_length=100)
    departure_time = models.TimeField()
    arrival_time = models.TimeField()
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
        return self.flight_duration - relativedelta(minutes=-10)
