from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404
from django.utils import timezone
from log.models import TechLogEntry
from log.views import ConsumablesSummary
from .models import Aeroplane
from .forms import AeroplaneForm


@login_required
def aeroplane(request, aeroplane_reg):
    ac = get_object_or_404(Aeroplane, registration=aeroplane_reg)
    form = AeroplaneForm(instance=ac)
    return render(request, "aeroplanes/aeroplane.html", {"aeroplane": ac, "last_check": ac.get_last_check(),
                                                         "form": form})


def _populate_consumables_usage_within_last(days, aeroplane):
    now = timezone.now()
    days_ago_x = now - timezone.timedelta(days=days)
    flights_in_x = TechLogEntry.objects.filter(aeroplane=aeroplane, departure_time__gt=days_ago_x)

    consumables_in_x = ConsumablesSummary()
    for flight in flights_in_x:
        consumables_in_x.airborne += flight.airborne_time
        consumables_in_x.fuel += flight.fuel_uplift
        consumables_in_x.oil += flight.oil_uplift
    return consumables_in_x


@login_required
def consumables(request, aeroplane_reg):
    ac = get_object_or_404(Aeroplane, registration=aeroplane_reg)

    consumables_usage_map = {
        30: _populate_consumables_usage_within_last(30, ac),
        60: _populate_consumables_usage_within_last(60, ac),
        90: _populate_consumables_usage_within_last(90, ac),
        120: _populate_consumables_usage_within_last(120, ac),
    }

    return render(request, "aeroplanes/consumables.html", {"aeroplane": ac, "consumables": consumables_usage_map})
