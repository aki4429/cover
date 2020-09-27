from django import forms

from .models import Locdata, Shiji, LocStatus

class LocForm(forms.ModelForm):

    class Meta:
        model = Locdata
        fields = ('banch', 'code','qty',)

class ShijiForm(forms.ModelForm):
    class Meta:
        model = Shiji
        fields = ('shiji_date', 'file_name', )

class LocStatusForm(forms.ModelForm):

    class Meta:
        model = LocStatus
        fields = ('koshinbi', 'shijibi',)

