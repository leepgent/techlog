from datetimewidget.widgets import DateTimeWidget, DateWidget
from django import forms

__author__ = 'lee'

from django.forms import ModelForm, modelform_factory
from .models import TechLogEntry

TechLogEntryForm = modelform_factory(TechLogEntry, fields=[
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
        ], widgets={
    "fuel_uplift": forms.NumberInput(attrs={'class': 'form-control'}),
    "oil_uplift": forms.NumberInput(attrs={'class': 'form-control'}),
    "departure_tacho": forms.NumberInput(attrs={'class': 'form-control'}),
    "arrival_tacho": forms.NumberInput(attrs={'class': 'form-control'}),
    "check_a_completed": forms.CheckboxInput(attrs={'class': 'form-control'}),
    "commander": forms.TextInput(attrs={'class': 'form-control'}),
    "departure_location": forms.TextInput(attrs={'class': 'form-control'}),
    "arrival_location": forms.TextInput(attrs={'class': 'form-control'}),
    "defects": forms.TextInput(attrs={'class': 'form-control'}),
    "departure_time": DateTimeWidget(attrs={'id':'departure_time_id'}, usel10n=True, bootstrap_version=3),
    "arrival_time": DateTimeWidget(attrs={'id':'arrival_time_id'}, usel10n=True, bootstrap_version=3)
})
