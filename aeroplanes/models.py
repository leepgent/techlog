from datetime import date, timedelta
from django.db import models
from django.conf import settings
from django.contrib.auth.models import Group


class Aeroplane(models.Model):
    CHECK_TYPE_50_HOURS_1 = "50HOURS1"
    CHECK_TYPE_50_HOURS_2 = "50HOURS2"
    CHECK_TYPE_150_HOURS = "150HOURS"
    CHECK_TYPE_ANNUAL = "ANNUAL"

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

    last_check = models.DateField()
    last_check_type = models.CharField(choices=CHECK_TYPE_CHOICES, max_length=20)
    last_annual = models.DateField()
    arc_expiry = models.DateField()
    insurance_expiry = models.DateField()

    def __unicode__(self):
        return "{0} ({1})".format(self.registration, self.model)

    def next_annual(self):
        n = self.last_annual
        y = timedelta(weeks=52)
        return n + y

    def next_check_type(self):
        last = self.last_check_type
        if last == self.CHECK_TYPE_50_HOURS_1:
            next_type = self.CHECK_TYPE_50_HOURS_2
        if last == self.CHECK_TYPE_50_HOURS_2:
            next_type = self.CHECK_TYPE_150_HOURS
        if last == self.CHECK_TYPE_150_HOURS:
            next_type = self.CHECK_TYPE_50_HOURS_1

        return next_type

    def next_check_in_hours(self):
        return 99
