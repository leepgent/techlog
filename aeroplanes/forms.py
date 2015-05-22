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
                'last_check',
                'last_check_type',
                'last_check_ttaf',
                'last_annual',
                'opening_tte',
                'opening_airframe_hours_after_last_check',
                'arc_expiry',
                'insurance_expiry'
            ]
