from django import forms

from .models import Locdata

class LocForm(forms.ModelForm):

    class Meta:
        model = Locdata
        fields = ('banch', 'code','qty',)