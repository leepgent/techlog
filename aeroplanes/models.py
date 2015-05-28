from datetime import date, timedelta
from dateutil.relativedelta import relativedelta
from django.db import models
from django.conf import settings
from django.contrib.auth.models import Group
from django.db.models import Sum
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

    #last_check = models.DateField()
    #last_check_type = models.CharField(choices=CHECK_TYPE_CHOICES, max_length=20)
    #last_check_ttaf = models.FloatField()  # hours and hundredths of hours
    last_annual = models.DateTimeField()

    opening_tte = models.FloatField()  # hours and hundredths of hours

    #opening_airframe_hours_after_last_check = models.FloatField()  # hours and decimal fraction of hours

    arc_expiry = models.DateField()
    insurance_expiry = models.DateField()

    def __unicode__(self):
        return "{0} ({1})".format(self.registration, self.model)

    @property
    def last_check(self):
        since = self.check_set.order_by("time").last()
        return since.time

    @property
    def last_check_type(self):
        since = self.check_set.order_by("time").last()
        return since.type

    @property
    def last_check_ttaf(self):
        since = self.check_set.order_by("time").last()
        return since.ttaf

    @property
    def flown_hours_since_check(self):
        #  Sum of tech log entries
        # TODO: remove circular dependency :-/
        last_check = self.check_set.order_by("time").last()

        entries = self.techlogentry_set.filter(departure_time__gt=last_check.time)
        hours = reduce(lambda h, entry: h+entry.airborne_time, list(entries), timezone.timedelta(0))  #  Can't use Django Aggregate/Sum because time isn't stored in DB
        hours_in_decimal = hours.total_seconds() / (60*60)  # Like our stored DB 'hours' values, we need hours + decimal fraction of hours
        return last_check.opening_hours_after_this_check + hours_in_decimal

    @property
    def next_check_pair(self):
        check_pair = self.calc_next_check_pair(self.last_check, self.last_annual, self.last_check_type, self.last_check_ttaf, self.flown_hours_since_check)
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
