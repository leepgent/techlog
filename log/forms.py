from datetimewidget.widgets import DateTimeWidget
from django import forms
from django.forms import widgets

__author__ = 'lee'

from django.forms import ModelForm
from .models import TechLogEntry


class TechLogEntryForm(ModelForm):
    commander = forms.ChoiceField(widget=widgets.Select(attrs={'class': 'form-control'}))

    class Meta:
        model = TechLogEntry
        fields = [
            "commander",
            "departure_location",
            "arrival_location",
            "departure_time",
            "arrival_time",
            "departure_tacho",
            "arrival_tacho",
            "fuel_uplift",
            "oil_uplift",
            "defects",
            "check_a_completed",
            "consumables_receipt_image"
        ]
        widgets = {
            "fuel_uplift": widgets.NumberInput(attrs={'class': 'form-control'}),
            "oil_uplift": widgets.NumberInput(attrs={'class': 'form-control'}),
            "departure_tacho": widgets.NumberInput(attrs={'class': 'form-control'}),
            "arrival_tacho": widgets.NumberInput(attrs={'class': 'form-control'}),
            "check_a_completed": widgets.CheckboxInput(attrs={'class': 'form-control'}),
            "departure_location": widgets.TextInput(attrs={'class': 'form-control'}),
            "arrival_location": widgets.TextInput(attrs={'class': 'form-control'}),
            "defects": widgets.TextInput(attrs={'class': 'form-control'}),
            "departure_time": DateTimeWidget(attrs={'id': 'departure_time_id'}, usel10n=True, bootstrap_version=3),
            "arrival_time": DateTimeWidget(attrs={'id': 'arrival_time_id'}, usel10n=True, bootstrap_version=3),
            "consumables_receipt_image": widgets.ClearableFileInput(attrs={'class': 'form-control'})
        }
