from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect, HttpResponseForbidden
from django.shortcuts import render, get_object_or_404

# Create your views here.
from django.utils import timezone
from aeroplanes.models import Aeroplane
from log.forms import TechLogEntryForm
from .models import TechLogEntry


@login_required
def log_entries(request, aeroplane_reg, year=None, month=None):
    now = timezone.now()
    if month is None:
        month = now.month
    if year is None:
        year = now.year

    d = timezone.datetime(year=year, month=month, day=1)

    aeroplane = get_object_or_404(Aeroplane, registration=aeroplane_reg)
    log_entry_list = TechLogEntry.objects.filter(aeroplane=aeroplane, departure_time__year=year, departure_time__month=month).order_by('departure_time')
    return render(request, "log/techlogentry_list.html", {"aeroplane": aeroplane, "date": d, "logentries": log_entry_list})


@login_required
def view_entry(request, aeroplane_reg, pk):
    aeroplane = get_object_or_404(Aeroplane, registration=aeroplane_reg)
    entry = get_object_or_404(TechLogEntry, pk=pk)

    if request.method == 'GET':
        form = TechLogEntryForm(instance=entry)

    elif request.method == 'POST':
        form = TechLogEntryForm(request.POST, instance=entry)
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

    elif request.method == "POST":
        form = TechLogEntryForm(request.POST)
        if form.is_valid():
            entry = form.save(commit=False)
            entry.aeroplane = aeroplane
            entry.owner = request.user
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


def month_summary(request, aeroplane_reg, year=None, month=None):
    now = timezone.now()
    if month is None:
        month = now.month
    if year is None:
        year = now.year

    d = timezone.datetime(year=year, month=month, day=1)

    aeroplane = get_object_or_404(Aeroplane, registration=aeroplane_reg)
    log_entry_list = TechLogEntry.objects.filter(aeroplane=aeroplane, departure_time__year=year, departure_time__month=month).order_by('departure_time')
    return render(request, "log/techlogentry_month_summary.html", {"aeroplane": aeroplane, "date": d, "logentries": log_entry_list})