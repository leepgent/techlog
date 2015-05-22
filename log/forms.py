from django import forms

__author__ = 'lee'

from django.forms import ModelForm, modelform_factory
from .models import TechLogEntry

TechLogEntryForm = modelform_factory(TechLogEntry, fields=[

            "date",
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
            "check_a_completed"
        ], widgets={
    "commander": forms.TextInput,
    "departure_location": forms.TextInput,
    "arrival_location": forms.TextInput,
    "defects": forms.TextInput

})

