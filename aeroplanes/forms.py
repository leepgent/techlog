from django.forms import ModelForm
from .models import Aeroplane

__author__ = 'Lee.Gent'

class AeroplaneForm(ModelForm):
    class Meta:
        model = Aeroplane
        fields =\
            [
                'owning_group',
                'registration',
                'registered',
                'manufacturer',
                'type',
                'model',
                'mtow',
                'built',
                'engine_count',
                'engine',
                'propeller',
                'last_annual',
                'opening_tte',
                'arc_expiry',
                'radio_expiry',
                'insurance_expiry'
            ]
