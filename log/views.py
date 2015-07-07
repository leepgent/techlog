from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.db.models import F, Value, Sum, Count, Q
from django.http import HttpResponseRedirect, HttpResponseForbidden
from django.shortcuts import render, get_object_or_404

# Create your views here.
from django.utils import timezone
from aeroplanes.models import Aeroplane
from group.models import GroupMemberProfile
from log.forms import TechLogEntryForm
from .models import TechLogEntry


@login_required
def log_entries_redirect(request, aeroplane_reg):
    now = timezone.now()
    month = now.month
    year = now.year

    return HttpResponseRedirect(reverse('techlogentrylist_by_date', args=[aeroplane_reg, year, month]))

@login_required
def log_entries(request, aeroplane_reg, year=None, month=None):
    now = timezone.now()
    if month is None:
        month = now.month
    else:
        month = int(month)
    if year is None:
        year = now.year
    else:
        year = int(year)

    d = timezone.datetime(year=year, month=month, day=1)

    aeroplane = get_object_or_404(Aeroplane, registration=aeroplane_reg)
    log_entry_list = TechLogEntry.objects.filter(aeroplane=aeroplane, departure_time__year=year, departure_time__month=month).order_by('departure_time')
    return render(request, "log/techlogentry_list.html", {"aeroplane": aeroplane, "date": d, "logentries": log_entry_list})

def get_commander_choices(owning_group):
    names = owning_group.user_set.all().values_list("last_name")
    cmdrs = [(c[0].capitalize(), c[0].capitalize()) for c in names]
    return cmdrs

@login_required
def view_entry(request, aeroplane_reg, pk):
    aeroplane = get_object_or_404(Aeroplane, registration=aeroplane_reg)
    group = aeroplane.owning_group
    entry = get_object_or_404(TechLogEntry, pk=pk)

    if request.method == 'GET':
        form = TechLogEntryForm(instance=entry)
        form.fields["commander"].choices = get_commander_choices(group)
    elif request.method == 'POST':
        form = TechLogEntryForm(request.POST, request.FILES, instance=entry)
        form.fields["commander"].choices = get_commander_choices(group)
        if form.is_valid():
            entry = form.save(commit=False)
            entry.aeroplane = aeroplane
            entry.owner = request.user
            entry.save()
            return HttpResponseRedirect(reverse("techlogentrylist", args=[aeroplane.registration]))

    return render(request, "log/techlogentry_detail.html", {"aeroplane": aeroplane, "form": form, "entry": entry})


@login_required
def add_flight(request, aeroplane_reg):
    aeroplane = get_object_or_404(Aeroplane, registration=aeroplane_reg)
    group = aeroplane.owning_group
    group_profile = group.groupprofile
    user = request.user
    memberprofile = GroupMemberProfile.objects.get(group=group_profile, member=user)

    if request.method == "GET":
        last_entry = aeroplane.techlogentry_set.order_by("departure_time").last()
        now = timezone.now().replace(second=0)
        form = TechLogEntryForm(initial={
            "departure_time": now,
            "arrival_time": now,
            "commander": request.user.last_name,
            "departure_location": last_entry.arrival_location,
            "fuel_uplift": 0,
            "oil_uplift": 0,
            "defects": "Nil",
            "departure_tacho": "{0:.2f}".format(last_entry.arrival_tacho)}
        )

        form.fields["commander"].choices = get_commander_choices(group)

    elif request.method == "POST":
        form = TechLogEntryForm(request.POST, request.FILES)
        form.fields["commander"].choices = get_commander_choices(group)
        if form.is_valid():
            entry = form.save(commit=False)
            entry.aeroplane = aeroplane
            entry.fuel_rebate_price_per_litre = group_profile.current_fuel_rebate_price_per_litre
            entry.oil_rebate_price_per_litre = group_profile.oil_rebate_price_per_litre
            entry.rate_includes_fuel = memberprofile.current_rate_includes_fuel
            entry.rate_includes_oil = memberprofile.current_rate_includes_oil
            entry.charge_regime = memberprofile.current_charge_regime
            entry.cost_per_unit = memberprofile.current_cost_per_unit
            entry.save()
            return HttpResponseRedirect(reverse("techlogentrylist", args=[aeroplane.registration]))

    return render(request, "log/techlogentry_add.html", {"aeroplane": aeroplane, "form": form})

@login_required
def delete_logentry(request, aeroplane_reg, pk):
    entry = get_object_or_404(TechLogEntry, pk=pk)
    if entry.owner.id != request.user.id:
        return HttpResponseForbidden()
    entry.delete()
    return HttpResponseRedirect(reverse("techlogentrylist", args=[aeroplane_reg]))


class SummaryTotals(object):
    def __init__(self):
        self.block = timezone.timedelta()
        self.tacho = 0
        self.fuel = 0
        self.oil = 0
        self.gross = 0
        self.fuel_rebate = 0
        self.oil_rebate = 0
        self.net = 0


class CommanderMonthSummary(object):
    def __init__(self):
        self.totals = SummaryTotals()
        self.flight_list = None


class ConsumablesSummary(object):
    def __init__(self):
        self.airborne = timezone.timedelta()
        self.fuel = 0
        self.oil = 0

    @property
    def fuel_litres_per_hour(self):
        consump = self.fuel / (self.airborne.total_seconds() / (60 * 60))
        return consump

    @property
    def oil_litres_per_hour(self):
        consump = self.oil / (self.airborne.total_seconds() / (60 * 60))
        return consump



def month_summary(request, aeroplane_reg, year=None, month=None):
    now = timezone.now()
    if month is None:
        month = now.month
    else:
        month = int(month)
    if year is None:
        year = now.year
    else:
        year = int(year)

    d = timezone.datetime(year=year, month=month, day=1)

    aeroplane = get_object_or_404(Aeroplane, registration=aeroplane_reg)
    consumables_summary = ConsumablesSummary()

    this_months_commanders = TechLogEntry.objects.filter(aeroplane=aeroplane, departure_time__year=year, departure_time__month=month).order_by('commander').distinct('commander').values_list('commander')
    commander_list = dict()
    for commander_ in this_months_commanders:
        commander = commander_[0]
        flights = TechLogEntry.objects.filter(aeroplane=aeroplane, departure_time__year=year, departure_time__month=month, commander=commander).order_by('departure_time')
        summary = CommanderMonthSummary()
        summary.flight_list = flights
        commander_list[commander] = summary

        # Total up some figures. Eventually whack these calculations into the DB...
        for flight in flights:
            # need: total block, total tacho, total fuel, total oil, total gross, total rebate, total net
            summary.totals.block += flight.flight_duration
            summary.totals.tacho += flight.engine_duration
            summary.totals.fuel += flight.fuel_uplift
            summary.totals.oil += flight.oil_uplift
            summary.totals.gross += flight.gross_cost
            summary.totals.fuel_rebate += flight.fuel_rebate
            summary.totals.oil_rebate += flight.oil_rebate
            summary.totals.net += flight.net_cost

            consumables_summary.airborne += flight.airborne_time
            consumables_summary.fuel += flight.fuel_uplift
            consumables_summary.oil += flight.oil_uplift

        #commander_list.append(flights)
    #log_entry_list = TechLogEntry.objects.filter(aeroplane=aeroplane, departure_time__year=year, departure_time__month=month).order_by('commander')
    return render(request, "log/techlogentry_month_summary.html", {"aeroplane": aeroplane, "date": d, "logentries": commander_list, "consumables_summary": consumables_summary})

SECS_IN_HOUR=60*60
def decimalise_time(timedelta):
    seconds = timedelta.total_seconds()
    return seconds / SECS_IN_HOUR

def cap398(request, aeroplane_reg, year=None, month=None):
    now = timezone.now()
    if month is None:
        month = now.month
    else:
        month = int(month)
    if year is None:
        year = now.year
    else:
        year = int(year)

    d = timezone.datetime(year=year, month=month, day=1)
    last_month_delta = timezone.timedelta(days=1)
    last_month = d - last_month_delta

    aeroplane = get_object_or_404(Aeroplane, registration=aeroplane_reg)

    # Get the last log entry for last month to find the base TTAF:
    #last_month = month-1
    #last_month_year = year
    #if last_month < 1:
    #    last_month = 12
    #    last_month_year = last_month_year - 1
    last_of_last_month = TechLogEntry.objects.filter(aeroplane=aeroplane, departure_time__year=last_month.year, departure_time__month=last_month.month).order_by('departure_time').last()
    if last_of_last_month is None:
        last_ttaf = aeroplane.opening_time
    else:
        last_ttaf = last_of_last_month.ttaf

    log_entry_list = TechLogEntry.objects.filter(aeroplane=aeroplane, departure_time__year=year, departure_time__month=month).order_by('departure_time')
    day_list = log_entry_list.datetimes('departure_time', 'day')
    #margin = timezone.timedelta(minutes=10)
    stat_list = list()
    #last_ttaf = 2660.25
    for day in day_list:
        day_stats = log_entry_list.filter(departure_time__day=day.day).annotate(db_block_time=(F('arrival_time') - F('departure_time'))).annotate(db_airborne_time=F('db_block_time')-Value("PT10M")).aggregate(total_airborne=Sum('db_airborne_time'), flight_count=Count("*"))
        day_stats["day"] = day
        day_stats["ttaf"] = last_ttaf + decimalise_time(day_stats["total_airborne"])
        last_ttaf = day_stats["ttaf"]
        stat_list.append(day_stats)

    return render(request, "log/techlogentry_cap398.html", {"aeroplane": aeroplane, "date": d, "stat_list": stat_list})
