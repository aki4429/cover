from django import forms

from .models import Locdata, Shiji, LocStatus, Pick

from .p2d import p2d

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

class OrderChoiceForm(forms.Form):
    choice1 = forms.fields.ChoiceField(
        choices = (
            ('banch', '番地'),
            ('code', 'コード'),
        ),
        required=True,
        widget=forms.widgets.Select
    )

class ChoiceForm(forms.Form):
    seisan = forms.ChoiceField(
        label = '生産日',
        choices = p2d(),
        widget=forms.widgets.Select,
        )
