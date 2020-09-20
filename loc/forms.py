from django import forms

from .models import Locdata, Shiji

class LocForm(forms.ModelForm):

    class Meta:
        model = Locdata
        fields = ('banch', 'code','qty',)

class ShijiForm(forms.ModelForm):
    class Meta:
        model = Shiji
        fields = ('file_name', 'seisan_shiji', )
