from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect, HttpResponseForbidden
from django.shortcuts import render, get_object_or_404

# Create your views here.
from django.utils import timezone
from django.views.generic import ListView, DetailView
from aeroplanes.models import Aeroplane
from log.forms import TechLogEntryForm
from .models import TechLogEntry


#  c.f. https://docs.djangoproject.com/en/1.8/topics/class-based-views/generic-display/
class LogEntryList(ListView):
    def get_queryset(self):
        self.aeroplane = get_object_or_404(Aeroplane, registration=self.kwargs["aeroplane_reg"])
        return TechLogEntry.objects.filter(aeroplane=self.aeroplane)


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
        last_entry = aeroplane.techlogentry_set.last()
        form = TechLogEntryForm(initial={
            "date": timezone.now().date(),
            "departure_time": timezone.now(),
            "arrival_time": timezone.now(),
            "commander": request.user.last_name,
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
