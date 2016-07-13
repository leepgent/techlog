from datetimewidget.widgets import DateTimeWidget
from django import forms
from django.forms import widgets, inlineformset_factory, ModelForm

from .models import TechLogEntry, ConsumablesReceipt


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
            "fuel_rebate_price_per_litre",
            "oil_rebate_price_per_litre"
        ]
        widgets = {
            "fuel_rebate_price_per_litre": widgets.NumberInput(attrs={'class': 'form-control'}),
            "oil_rebate_price_per_litre": widgets.NumberInput(attrs={'class': 'form-control'}),
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
        }

InlineConsumablesReceiptFormSet = inlineformset_factory(
        TechLogEntry,
        ConsumablesReceipt,
        fields=('image',),
        extra=2,
        widgets={"image": widgets.ClearableFileInput(attrs={'class': 'form-control'})}
)
