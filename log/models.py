from django.conf import settings
from django.db import models
from django.db.models import F, Value, Sum
from django.utils import timezone
from aeroplanes.models import Aeroplane, decimalise_timedelta
from group.models import GroupProfile


class TechLogEntry(models.Model):
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
    consumables_receipt_image = models.ImageField(null=True, blank=True)

    fuel_rebate_price_per_litre = models.FloatField()
    oil_rebate_price_per_litre = models.FloatField()
    rate_includes_fuel = models.BooleanField()
    rate_includes_oil = models.BooleanField()
    charge_regime = models.CharField(max_length=20, choices=GroupProfile.CHARGE_REGIME_CHOICES)
    cost_per_unit = models.FloatField()

    def __unicode__(self):
        return "Flight in {0} by {1} at {2}".format(self.aeroplane, self.commander, self.departure_time)

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
        # Opening time + sum of times up to and including myself
        logged_dict = self.aeroplane.techlogentry_set.all().filter(departure_time__lte=self.departure_time).annotate(db_block_time=(F('arrival_time') - F('departure_time'))).annotate(db_airborne_time=F('db_block_time')-Value("PT10M")).aggregate(total_logged_airborne=Sum('db_airborne_time'))
        logged = logged_dict["total_logged_airborne"]
        return self.aeroplane.opening_time + decimalise_timedelta(logged)

        #since = self.aeroplane.check_set.filter(time__lte=self.departure_time).order_by("time").last()
        #entries = self.aeroplane.techlogentry_set.filter(arrival_time__gte=since.time, arrival_time__lte=self.arrival_time)
        #hours = reduce(lambda h, entry: h+entry.airborne_time, list(entries), timezone.timedelta(0))
        #hours_in_decimal = hours.total_seconds() / (60*60)
        #return since.ttaf + since.opening_hours_after_this_check + hours_in_decimal

    @property
    def until_next_check(self):
        # next check ttaf - my ttaf
        #last_check = self.aeroplane.get_last_check()
        #next_check_ttaf = self.aeroplane.next_flying_hours_check.check_at_total_flying_hours
        #remaining = next_check_ttaf - self.ttaf
        #return remaining

        since = self.aeroplane.get_last_check_from(self.departure_time)
        next_check = since.ttaf + Aeroplane.MAX_HOURS_BETWEEN_CHECKS

        #since = self.aeroplane.check_set.filter(time__lte=self.departure_time).order_by("time").last()

        entries = self.aeroplane.techlogentry_set.filter(arrival_time__lte=self.arrival_time)
        # TODO: use DB aggregate
        hours = reduce(lambda h, entry: h+entry.airborne_time, list(entries), timezone.timedelta(0))  #  Can't use Django Aggregate/Sum because time isn't stored in DB
        hours_in_decimal = hours.total_seconds() / (60*60)  # Like our stored DB 'hours' values, we need hours + decimal fraction of hours

        return next_check - hours_in_decimal - self.aeroplane.opening_time

    @property
    def gross_cost(self):
        rate = self.cost_per_unit

        if self.charge_regime == GroupProfile.CHARGE_REGIME_TACHO_HOURS:
            cost = self.engine_duration * rate
        else:
            cost = 0

        return cost

    @property
    def fuel_rebate(self):
        if self.rate_includes_fuel:
            return self.fuel_rebate_price_per_litre * self.fuel_uplift
        return 0

    @property
    def oil_rebate(self):
        if self.rate_includes_oil:
            return self.oil_rebate_price_per_litre * self.oil_uplift
        return 0

    @property
    def rebate(self):
        return self.fuel_rebate + self.oil_rebate

    @property
    def net_cost(self):
        return self.gross_cost - self.rebate
