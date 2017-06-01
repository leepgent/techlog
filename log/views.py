from __future__ import unicode_literals

from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.db.models import F, Value, Sum, Count, Q
from django.http import HttpResponseRedirect, HttpResponseForbidden, HttpResponse
from django.shortcuts import render, get_object_or_404

from django.utils import timezone
from django.core import serializers
from django.utils.html import escape

from aeroplanes.models import Aeroplane
from group.models import GroupMemberProfile
from .forms import TechLogEntryForm, InlineConsumablesReceiptFormSet
from .models import TechLogEntry


@login_required
def log_entries_redirect(request, aeroplane_reg):
    now = timezone.now()
    month = now.month
    year = now.year

    return HttpResponseRedirect(reverse('techlogentrylist_by_date', args=[aeroplane_reg, year, month]))


def _generate_back_forward_date_links(base_view_name, aeroplane_reg, year, month):
    next_month_year = year
    next_month_month = month + 1
    if next_month_month > 12:
        next_month_month = 1
        next_month_year += 1

    next_month_date = timezone.datetime(year=next_month_year, month=next_month_month, day=1)

    last_month_year = year
    last_month_month = month - 1
    if last_month_month < 1:
        last_month_month = 12
        last_month_year -= 1

    last_month_date = timezone.datetime(year=last_month_year, month=last_month_month, day=1)

    next_year_date = timezone.datetime(year=year + 1, month=month, day=1)
    last_year_date = timezone.datetime(year=year - 1, month=month, day=1)

    next_month_link = reverse(base_view_name, args=(aeroplane_reg, next_month_date.year, next_month_date.month))
    last_month_link = reverse(base_view_name, args=(aeroplane_reg, last_month_date.year, last_month_date.month))
    next_year_link = reverse(base_view_name, args=(aeroplane_reg, next_year_date.year, next_year_date.month))
    last_year_link = reverse(base_view_name, args=(aeroplane_reg, last_year_date.year, last_year_date.month))

    context_dict = {
        "next_month_date": next_month_date,
        "last_month_date": last_month_date,
        "next_year_date": next_year_date,
        "last_year_date": last_year_date,
        "last_month_link": last_month_link,
        "next_month_link": next_month_link,
        "last_year_link": last_year_link,
        "next_year_link": next_year_link
    }

    return context_dict


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
    date_link_dict = _generate_back_forward_date_links('techlogentrylist_by_date', aeroplane_reg, year, month)

    context_dict = {
        "aeroplane": aeroplane,
        "date": d,
        "logentries": log_entry_list
    }
    context_dict.update(date_link_dict)

    return render(request, "log/techlogentry_list.html", context_dict)


def _commanderise_user(user):
    return _commanderise(user.first_name, user.last_name)


def _commanderise(first_name, last_name):
    return "{1}, {0}".format(first_name.capitalize()[0], last_name.capitalize())


def _get_commander_choices(owning_group):
    names = owning_group.user_set.filter(is_active=True).values_list("first_name", "last_name")

    cmdrs = []

    for n in names:
        cmdr = _commanderise(n[0], n[1])
        cmdrs.append((cmdr, cmdr))

    return cmdrs


@login_required
def view_entry(request, aeroplane_reg, pk):
    aeroplane = get_object_or_404(Aeroplane, registration=aeroplane_reg)
    group = aeroplane.owning_group
    entry = get_object_or_404(TechLogEntry, pk=pk)

    if request.method == 'GET':
        form = TechLogEntryForm(instance=entry)
        receipts_form = InlineConsumablesReceiptFormSet(instance=entry)
        form.fields["commander"].choices = _get_commander_choices(group)
    elif request.method == 'POST':
        form = TechLogEntryForm(request.POST, request.FILES, instance=entry)
        receipt_formset = InlineConsumablesReceiptFormSet(request.POST, request.FILES, instance=entry)
        form.fields["commander"].choices = _get_commander_choices(group)
        if form.is_valid():
            entry = form.save(commit=False)
            entry.aeroplane = aeroplane
            entry.save()

            if receipt_formset.is_valid():
                receipt_formset.instance = entry
                receipt_formset.save()

            return HttpResponseRedirect(reverse("techlogentrylist", args=[aeroplane.registration]))

    return render(request, "log/techlogentry_detail.html", {"aeroplane": aeroplane, "form": form, "receipts_form": receipts_form, "entry": entry})


@login_required
def add_flight(request, aeroplane_reg):
    aeroplane = get_object_or_404(Aeroplane, registration=aeroplane_reg)
    group = aeroplane.owning_group
    group_profile = group.groupprofile
    user = request.user
    memberprofile = GroupMemberProfile.objects.get(group=group_profile, member=user)

    context = dict()
    context['aeroplane'] = aeroplane

    if request.method == "GET":
        last_entry = aeroplane.techlogentry_set.order_by("departure_time").last()
        now = timezone.now().replace(second=0)
        form = TechLogEntryForm(initial={
            "departure_time": now,
            "arrival_time": now,
            "commander": _commanderise_user(request.user),
            "departure_location": last_entry.arrival_location,
            "fuel_uplift": 0,
            "oil_uplift": 0,
            "defects": "Nil",
            "departure_tacho": "{0:.2f}".format(last_entry.arrival_tacho),
            "fuel_rebate_price_per_litre": group_profile.current_fuel_rebate_price_per_litre,
            "oil_rebate_price_per_litre": group_profile.current_oil_rebate_price_per_litre
        }
        )

        form.fields["commander"].choices = _get_commander_choices(group)

        receipt_formset = InlineConsumablesReceiptFormSet()

        context['form'] = form
        context['receipt_formset'] = receipt_formset

    elif request.method == "POST":
        form = TechLogEntryForm(request.POST, request.FILES)
        receipt_formset = InlineConsumablesReceiptFormSet(request.POST, request.FILES)
        form.fields["commander"].choices = _get_commander_choices(group)

        context['form'] = form
        context['receipt_formset'] = receipt_formset

        if form.is_valid():
            entry = form.save(commit=False)
            entry.aeroplane = aeroplane
            entry.rate_includes_fuel = memberprofile.current_rate_includes_fuel
            entry.rate_includes_oil = memberprofile.current_rate_includes_oil
            entry.charge_regime = memberprofile.current_charge_regime
            entry.cost_per_unit = memberprofile.current_cost_per_unit
            entry.save()

            if receipt_formset.is_valid():
                receipt_formset.instance = entry
                receipt_formset.save()

            return HttpResponseRedirect(reverse("techlogentrylist", args=[aeroplane.registration]))

    return render(request, "log/techlogentry_add.html", context)


@login_required
def delete_logentry(request, aeroplane_reg, pk):
    entry = get_object_or_404(TechLogEntry, pk=pk)
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
        if not self.airborne.total_seconds() > 0:
            return 0.0
        consump = self.fuel / (self.airborne.total_seconds() / (60 * 60))
        return consump

    @property
    def oil_litres_per_hour(self):
        if not self.airborne.total_seconds() > 0:
            return 0.0
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

    date_link_dict = _generate_back_forward_date_links('log_month_summary', aeroplane_reg, year, month)
    context = {
        "aeroplane": aeroplane,
        "date": d,
        "logentries": commander_list,
        "consumables_summary": consumables_summary
    }
    context.update(date_link_dict)

    return render(request, "log/techlogentry_month_summary.html", context)

SECS_IN_HOUR=60*60


def _decimalise_time(timedelta):
    seconds = timedelta.total_seconds()
    return seconds / SECS_IN_HOUR


def cap398(request, aeroplane_reg, year=None, month=None):
    return _cap398(request, "log/techlogentry_cap398.html", aeroplane_reg, year, month)


def cap398_print(request, aeroplane_reg, year=None, month=None):
    return _cap398(request, "log/techlogentry_cap398.print.html", aeroplane_reg, year, month)


def _cap398(request, template, aeroplane_reg, year=None, month=None):
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
    last_of_last_month = TechLogEntry.objects.filter(aeroplane=aeroplane, departure_time__year=last_month.year, departure_time__month=last_month.month).order_by('departure_time').last()
    if last_of_last_month is None:
        last_ttaf = aeroplane.opening_time
        last_tte = aeroplane.opening_tte
        last_ttp = aeroplane.opening_ttp
    else:
        last_ttaf = last_of_last_month.ttaf
        last_tte = last_of_last_month.tte
        last_ttp = last_of_last_month.ttp

    log_entry_list = TechLogEntry.objects.filter(aeroplane=aeroplane, departure_time__year=year, departure_time__month=month).order_by('departure_time')
    day_list = log_entry_list.datetimes('departure_time', 'day')

    ten_minute_margin = Value("PT10M")
    stat_list = list()
    for day in day_list:
        day_stats = log_entry_list.filter(departure_time__day=day.day).annotate(db_block_time=(F('arrival_time') - F('departure_time'))).annotate(db_airborne_time=F('db_block_time')-ten_minute_margin).aggregate(total_airborne=Sum('db_airborne_time'), flight_count=Count("*"))
        day_stats["day"] = day
        day_stats["ttaf"] = last_ttaf + _decimalise_time(day_stats["total_airborne"])
        day_stats["tte"] = last_tte + _decimalise_time(day_stats["total_airborne"])
        day_stats["ttp"] = last_ttp + _decimalise_time(day_stats["total_airborne"])
        last_ttaf = day_stats["ttaf"]
        last_tte = day_stats["tte"]
        last_ttp = day_stats["ttp"]
        stat_list.append(day_stats)

    context = {
        "aeroplane": aeroplane,
        "date": d,
        "stat_list": stat_list
    }

    date_link_dict = _generate_back_forward_date_links('cap398_by_date', aeroplane_reg, year, month)
    context.update(date_link_dict)

    return render(request, template, context)


def log_entries_xml(request, aeroplane_reg, year=None, month=None):
    now = timezone.now()
    if month is None:
        month = now.month
    else:
        month = int(month)
    if year is None:
        year = now.year
    else:
        year = int(year)

    aeroplane = get_object_or_404(Aeroplane, registration=aeroplane_reg)
    log_entry_list = TechLogEntry.objects.filter(aeroplane=aeroplane, departure_time__year=year, departure_time__month=month).order_by('departure_time')

    response = HttpResponse(content_type='text/xml')
    response.write('<?xml version="1.0" encoding="UTF-8" ?>\n')
    response.write('<techlog-monthlog version="0.1" aeroplane="{}" year="{}" month="{}">\n'.format(aeroplane_reg, year, month))
    response.write('<!-- Hello Dave, looking for the old format? Add /v0.1 to this URL. -->\n')

    for entry in log_entry_list:
        response.write('\t<flight id="{}">\n'.format(entry.id))
        response.write('\t\t<commander>{}</commander>\n'.format(entry.commander))
        response.write('\t\t<departure_location>{}</departure_location>\n'.format(entry.departure_location))
        response.write('\t\t<arrival_location>{}</arrival_location>\n'.format(entry.arrival_location))
        response.write('\t\t<departure_time>{}</departure_time>\n'.format(entry.departure_time))
        response.write('\t\t<arrival_time>{}</arrival_time>\n'.format(entry.arrival_time))
        response.write('\t\t<departure_tacho>{}</departure_tacho>\n'.format(entry.departure_tacho))
        response.write('\t\t<arrival_tacho>{}</arrival_tacho>\n'.format(entry.arrival_tacho))
        response.write('\t\t<fuel_uplift>{}</fuel_uplift>\n'.format(entry.fuel_uplift))
        response.write('\t\t<oil_uplift>{}</oil_uplift>\n'.format(entry.oil_uplift))
        response.write('\t\t<defects>{}</defects>\n'.format(entry.defects))
        response.write('\t\t<check_a_completed>{}</check_a_completed>\n'.format('true' if entry.check_a_completed else 'false'))

        response.write('\t\t<fuel_rebate_price_per_litre>{}</fuel_rebate_price_per_litre>\n'.format(entry.fuel_rebate_price_per_litre))
        response.write('\t\t<oil_rebate_price_per_litre>{}</oil_rebate_price_per_litre>\n'.format(entry.oil_rebate_price_per_litre))
        response.write('\t\t<oil_rebate_price_per_litre>{}</oil_rebate_price_per_litre>\n'.format('true' if entry.rate_includes_fuel else 'false'))
        response.write('\t\t<rate_includes_oil>{}</rate_includes_oil>\n'.format('true' if entry.rate_includes_oil else 'false'))
        response.write('\t\t<charge_regime>{}</charge_regime>\n'.format(entry.charge_regime))
        response.write('\t\t<cost_per_unit>{}</cost_per_unit>\n'.format(entry.cost_per_unit))

        response.write('\t\t<consumables_receipts>\n')
        for receipt in entry.consumablesreceipt_set.all():
            encoded_url = escape(receipt.image.url)
            response.write('\t\t\t<receipt name="{}" url="{}" />\n'.format(receipt.image.name, encoded_url))

        response.write('\n\n</consumables_receipts>\n')

        response.write('\t</flight>\n')

    response.write('</techlog-monthlog>\n')

    return response


def log_entries_xml_v01(request, aeroplane_reg, year=None, month=None):
    now = timezone.now()
    if month is None:
        month = now.month
    else:
        month = int(month)
    if year is None:
        year = now.year
    else:
        year = int(year)

    aeroplane = get_object_or_404(Aeroplane, registration=aeroplane_reg)
    log_entry_list = TechLogEntry.objects.filter(aeroplane=aeroplane, departure_time__year=year, departure_time__month=month).order_by('departure_time')

    response = HttpResponse(content_type='text/xml')
    response.write('<?xml version="1.0" encoding="UTF-8" ?>\n')
    response.write('<django-objects version="1.0">\n')
    response.write('<!-- techlog-monthlog version="0.1" aeroplane="{}" year="{}" month="{}" -->\n'.format(aeroplane_reg, year, month))
    response.write('<!-- The use of this schema version is *deprecated*! -->\n')
    for entry in log_entry_list:
        response.write('\t<object pk="{}" model="log.techlogentry">\n'.format(entry.id))
        response.write('\t\t<field type="TextField" name="commander">{}</field>\n'.format(entry.commander))
        response.write('\t\t<field type="TextField" name="departure_location">{}</field>\n'.format(entry.departure_location))
        response.write('\t\t<field type="TextField" name="arrival_location">{}</field>\n'.format(entry.arrival_location))
        response.write('\t\t<field type="DateTimeField" name="departure_time">{}</field>\n'.format(entry.departure_time))
        response.write('\t\t<field type="DateTimeField" name="arrival_time">{}</field>\n'.format(entry.arrival_time))
        response.write('\t\t<field type="FloatField" name="departure_tacho">{}</field>\n'.format(entry.departure_tacho))
        response.write('\t\t<field type="FloatField" name="arrival_tacho">{}</field>\n'.format(entry.arrival_tacho))
        response.write('\t\t<field type="FloatField" name="fuel_uplift">{}</field>\n'.format(entry.fuel_uplift))
        response.write('\t\t<field type="FloatField" name="oil_uplift">{}</field>\n'.format(entry.oil_uplift))
        response.write('\t\t<field type="TextField" name="defects">{}</field>\n'.format(entry.defects))
        response.write('\t\t<field type="BooleanField" name="check_a_completed">{}</field>\n'.format(entry.check_a_completed))

        if entry.consumablesreceipt_set.exists():
            encoded_url = escape(entry.consumablesreceipt_set.first().image.url)
            response.write('\t\t<field type="FileField" name="consumables_receipt_image">{}</field>\n'.format(encoded_url))
        else:
            response.write('\t\t<field type="FileField" name="consumables_receipt_image"/>\n')
        response.write('\t\t<field type="FloatField" name="fuel_rebate_price_per_litre">{}</field>\n'.format(entry.fuel_rebate_price_per_litre))
        response.write('\t\t<field type="FloatField" name="oil_rebate_price_per_litre">{}</field>\n'.format(entry.oil_rebate_price_per_litre))
        response.write('\t\t<field type="BooleanField" name="oil_rebate_price_per_litre">{}</field>\n'.format(entry.rate_includes_fuel))
        response.write('\t\t<field type="BooleanField" name="rate_includes_oil">{}</field>\n'.format(entry.rate_includes_oil))
        response.write('\t\t<field type="CharField" name="charge_regime">{}</field>\n'.format(entry.charge_regime))
        response.write('\t\t<field type="FloatField" name="cost_per_unit">{}</field>\n'.format(entry.cost_per_unit))

        response.write('\t</object>\n')

    response.write('</django-objects>\n')

    return response


def log_entries_json(request, aeroplane_reg, year=None, month=None):
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
    payload = serializers.serialize("json", log_entry_list)
    return HttpResponse(payload, content_type='application/json')


@login_required
def log_entries_technical(request, aeroplane_reg, year=None, month=None):
    template = "log/techlogentry_list_technical.html"
    return _log_entries_technical(request, template, aeroplane_reg, year, month)


@login_required
def log_entries_technical_print(request, aeroplane_reg, year=None, month=None):
    template = "log/techlogentry_list_technical.print.html"
    return _log_entries_technical(request, template, aeroplane_reg, year, month)


def _log_entries_technical(request, template, aeroplane_reg, year=None, month=None):
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

    date_link_dict = _generate_back_forward_date_links('techlogentrylist_technical', aeroplane_reg, year, month)

    aeroplane = get_object_or_404(Aeroplane, registration=aeroplane_reg)
    log_entry_list = TechLogEntry.objects.filter(aeroplane=aeroplane, departure_time__year=year, departure_time__month=month).order_by('departure_time')
    context_dict = {
                      "aeroplane": aeroplane,
                      "date": d,
                      "logentries": log_entry_list
                  }
    context_dict.update(date_link_dict)

    return render(request, template, context_dict)


@login_required
def group_member_list(request, aeroplane_reg):
    aeroplane = get_object_or_404(Aeroplane, registration=aeroplane_reg)
    context = {
        'aeroplane': aeroplane
    }
    template = 'log/memberlist.html'
    return render(request, template, context)


@login_required
def group_member_statement(request, aeroplane_reg, member_id):
    aeroplane = get_object_or_404(Aeroplane, registration=aeroplane_reg)
    member = get_user_model().objects.get(pk=member_id)
    entries = aeroplane.techlogentry_set.filter(commander=_commanderise_user(member)).order_by('departure_time')  # WARNING WARNING WARNING LOOSE ASSOCIATION
    context = {
        'aeroplane': aeroplane,
        'member': member,
        'entries': entries
    }

    template = 'log/member_statement.html'
    return render(request, template, context)


@login_required
def group_member_statement_export(request, aeroplane_reg, member_id):
    aeroplane = get_object_or_404(Aeroplane, registration=aeroplane_reg)
    member = get_user_model().objects.get(pk=member_id)
    entries = aeroplane.techlogentry_set.filter(commander=_commanderise_user(member)).order_by('departure_time')  # WARNING WARNING WARNING LOOSE ASSOCIATION
    context = {
        'aeroplane': aeroplane,
        'member': member,
        'entries': entries
    }

    template = 'log/member_statement.csv'
    response = render(request, template, context, content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename={}.csv'.format(member.last_name)
    return response


@login_required
def dump_last_x_weeks(request, aeroplane_reg, weeks):
    now = timezone.now()
    weeks = int(weeks)
    delta = timezone.timedelta(weeks=weeks)
    then = now - delta
    aeroplane = get_object_or_404(Aeroplane, registration=aeroplane_reg)
    entries = aeroplane.techlogentry_set.filter(departure_time__gte=then).order_by('departure_time')

    context = {
        'aeroplane': aeroplane,
        'entries': entries
    }
    template = 'log/dump_weeks.csv'
    response = render(request, template, context, content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename={}-{}-weeks.csv'.format(aeroplane_reg, weeks)
    return response
