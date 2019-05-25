from django import forms
from server.models import *


class ParaModelForm(forms.ModelForm):
    class Meta:
        model = WorkingParameter
        fields = ['mode', 'Temp_highLimit', 'Temp_lowLimit', 'default_TargetTemp', 'FeeRate_H', 'FeeRate_M',
                  'FeeRate_L']


class ReportForm(forms.ModelForm):
    class Meta:
        model = Report
        fields = ['room', 'times_of_on_and_off', 'serving_duration', 'total_Fee', 'times_of_dispatch',
                  'number_of_RDR',
                  ' times_of_changeTemp', 'times_of_changeFanSpeed']
