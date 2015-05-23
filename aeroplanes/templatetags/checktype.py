from django import template
from ..models import Aeroplane
__author__ = 'lee.gent'

register = template.Library()


@register.filter
def humanise_checktype(check_type):
    for choice in Aeroplane.CHECK_TYPE_CHOICES:
        if choice[0] == check_type:
            return choice[1]
    return ""
