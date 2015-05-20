__author__ = 'lee'

from django.forms import ModelForm
from .models import TechLogEntry

class TechLogEntryForm(ModelForm):
    class Meta:
        model = TechLogEntry
        fields = [
            "aeroplane",
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
        ]
