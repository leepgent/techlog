from __future__ import unicode_literals
from datetime import date, timedelta
from dateutil.relativedelta import relativedelta
from django.db import models
from django.conf import settings
from django.contrib.auth.models import Group
from django.db.models import Sum, F, Value
from django.utils import timezone


class CalendarCheck(object):
    def __init__(self, check_type, check_before):
        self.check_type = check_type
        self.check_before = check_before


class FlyingHoursCheck(object):
    def __init__(self, check_type, check_in_flying_hours, check_at_flying_hours):
        self.check_type = check_type
        self.check_in_flying_hours = check_in_flying_hours
        self.check_at_total_flying_hours = check_at_flying_hours


class CheckPair(object):
    def __init__(self, flying_hours_check, calendar_check):
        self.flying_hours_check = flying_hours_check
        self.calendar_check = calendar_check


SECS_IN_HOUR=60*60
def decimalise_timedelta(timedelta):
    seconds = timedelta.total_seconds()
    return seconds / SECS_IN_HOUR


class Aeroplane(models.Model):
    MAX_HOURS_BETWEEN_CHECKS = 50
    MAX_MONTHS_BETWEEN_CHECKS = 6

    CHECK_TYPE_50_HOURS_1 = "50HOURS1"
    CHECK_TYPE_50_HOURS_2 = "50HOURS2"
    CHECK_TYPE_150_HOURS = "150HOURS"
    CHECK_TYPE_ANNUAL = "ANNUAL"

    NEXT_CHECK_MAP = {
            CHECK_TYPE_50_HOURS_1: CHECK_TYPE_50_HOURS_2,
            CHECK_TYPE_50_HOURS_2: CHECK_TYPE_150_HOURS,
            CHECK_TYPE_150_HOURS: CHECK_TYPE_50_HOURS_1,
            CHECK_TYPE_ANNUAL: CHECK_TYPE_50_HOURS_1
    }

    CHECK_TYPE_CHOICES = (
        (CHECK_TYPE_50_HOURS_1, "50 hours (first)"),
        (CHECK_TYPE_50_HOURS_2, "50 hours (second)"),
        (CHECK_TYPE_150_HOURS, "150 hours"),
        (CHECK_TYPE_ANNUAL, "Annual"),
    )

    owning_group = models.ForeignKey(Group)

    registration = models.CharField(max_length=10)
    registered = models.DateField()

    manufacturer = models.CharField(max_length=200)
    type = models.CharField(max_length=200)
    model = models.CharField(max_length=200)
    mtow = models.IntegerField()
    built = models.IntegerField()

    engine_count = models.IntegerField()
    engine = models.CharField(max_length=100)
    propeller = models.CharField(max_length=100)

    last_annual = models.DateTimeField()

    opening_tte = models.FloatField()  # hours and hundredths of hours
    opening_time = models.FloatField()

    arc_expiry = models.DateField()
    insurance_expiry = models.DateField()
    radio_expiry = models.DateField()

    def __unicode__(self):
        return "{0} ({1})".format(self.registration, self.model)

    def _generate_initial_check(self):
        c = Check()
        c.aeroplane = self
        c.time = self.last_annual
        c.type = self.CHECK_TYPE_ANNUAL
        c.ttaf = self.opening_time
        return c

    def get_last_check(self):
        last_check = self.check_set.order_by("time").last()
        if last_check is not None:
            return last_check
        # Oh! New 'plane?
        return self._generate_initial_check()

    def get_last_check_from(self, fromdate):
        last_check = self.check_set.filter(time__lte=fromdate).order_by("time").last()
        if last_check is not None:
            return last_check
        # Oh! New 'plane?
        return self._generate_initial_check()

    @property
    def ttaf(self):
        # Current TTAF is the TTAF at the last check [or opening number] + how many AF hours since
        last_check = self.get_last_check()

        logged_dict = self.techlogentry_set.filter(departure_time__gt=last_check.time).annotate(db_block_time=(F('arrival_time') - F('departure_time'))).annotate(db_airborne_time=F('db_block_time')-Value("PT10M")).aggregate(total_logged_airborne=Sum('db_airborne_time'))
        logged = logged_dict["total_logged_airborne"]
        if logged is None:
            logged = 0
        else:
            logged = decimalise_timedelta(logged)
        return last_check.ttaf + logged

    @property
    def flown_hours_since_check(self):
        #  Sum of tech log entries
        # TODO: remove circular dependency :-/

        # Total hours minus last check hours (if any)
        # Where total is all in logbook + opening total
        last_check = self.get_last_check()

        ttaf = self.ttaf

        flown_since_last_check = ttaf - last_check.ttaf

        return flown_since_last_check

    @property
    def next_flying_hours_check(self):
        last = self.get_last_check()
        next_flying_hours_check = self.calc_next_flying_hours_check(last.type, last.ttaf, self.flown_hours_since_check)
        return next_flying_hours_check

    @property
    def next_check_pair(self):
        last = self.get_last_check()
        check_pair = self.calc_next_check_pair(last.time, self.last_annual, last.type, last.ttaf, self.flown_hours_since_check)
        return check_pair

    @classmethod
    def calc_next_flying_hours_check(cls, last_check_type, last_check_ttaf, flown_hours):
        next_check_type = cls.NEXT_CHECK_MAP[last_check_type]
        next_check_in_flying_hours = cls.MAX_HOURS_BETWEEN_CHECKS - flown_hours
        next_check_at_ttaf_hours = cls.MAX_HOURS_BETWEEN_CHECKS + last_check_ttaf

        return FlyingHoursCheck(next_check_type, next_check_in_flying_hours, next_check_at_ttaf_hours)

    @classmethod
    def calc_next_calendar_check(cls, last_check_at, last_annual_check_at):
        next_annual_at = last_annual_check_at + relativedelta(years=+1)
        next_50hrs_at = last_check_at + relativedelta(months=+cls.MAX_MONTHS_BETWEEN_CHECKS)

        next_check_before, next_calendar_check_is = ((next_annual_at, Aeroplane.CHECK_TYPE_ANNUAL) if next_annual_at <= next_50hrs_at else (next_50hrs_at, Aeroplane.CHECK_TYPE_50_HOURS_1))

        return CalendarCheck(next_calendar_check_is, next_check_before)

    @classmethod
    def calc_next_check_pair(cls, last_check_at, last_annual_check_at, last_check_type, last_check_ttaf, flown_hours):
        next_flying_hours_check = cls.calc_next_flying_hours_check(last_check_type, last_check_ttaf, flown_hours)
        next_calendar_check = cls.calc_next_calendar_check(last_check_at, last_annual_check_at)

        return CheckPair(next_flying_hours_check, next_calendar_check)


class Check(models.Model):
    aeroplane = models.ForeignKey(Aeroplane)
    time = models.DateTimeField()
    type = models.CharField(max_length=10, choices=Aeroplane.CHECK_TYPE_CHOICES)
    ttaf = models.FloatField()

    def __unicode__(self):
        return "{0} check for {1} on {2} @ {3} TTAF".format(self.type, self.aeroplane, self.time, self.ttaf)

