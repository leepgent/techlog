from django import template
from django.utils import timezone

__author__ = 'lee.gent'

register = template.Library()


@register.filter
def humanise(decimal_hours):
    hours = int(decimal_hours)
    parts_of_hour = decimal_hours - hours
    minutes = 60 * parts_of_hour
    return timezone.timedelta(hours=hours, minutes=minutes)


@register.filter
def humanise_longhours(decimal_hours):
    hours = int(decimal_hours)
    parts_of_hour = decimal_hours - hours
    minutes = 60 * parts_of_hour
    minutes = int(round(minutes, 2))
    return "{0}.{1:02}".format(hours, minutes)
