from django import forms

from django.core.files.storage import default_storage
from django.core.validators import FileExtensionValidator

from .models import Locdata, Shiji, LocStatus, Pick, Kakutei

from .p2d import p2d
import os
from django.conf import settings

class LocForm(forms.ModelForm):

    class Meta:
        model = Locdata
        fields = ('banch', 'code','qty',)

class ShijiForm(forms.ModelForm):
    class Meta:
        model = Shiji
        fields = ('file_name', )

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


class InvUpForm(forms.Form):
    invf = forms.FileField(label='入荷インボイス',
        validators=[FileExtensionValidator(['xls' ])],
        #拡張子バリデーター。アップロードファイルの拡張子が違う時にエラー
        )

    def save(self):
        upload_file = self.cleaned_data['invf']
        #default_storage.location = os.path.join(settings.MEDIA_ROOT, 'inv')
        file_name = default_storage.save(upload_file.name, upload_file)
        #return default_storage.url(file_name)
        #file属性で返す。
        return default_storage.open(file_name), default_storage.url(file_name)


class KakuteiForm(forms.ModelForm):
    class Meta:
        model = Kakutei
        fields = [
                 'code',
                 'qty',
                 'loc_qty',
                 'seisan',
                 'om',
                 'banch',
                ]
        widgets = {
                'code': forms.Textarea(attrs={'rows':1, 'cols':45}),
                'qty': forms.Textarea(attrs={'rows':1, 'cols':10}),
                'loc_qty': forms.Textarea(attrs={'rows':1, 'cols':10}),
                'seisan':forms.DateInput(attrs={"type":"date"}),
                'om': forms.Textarea(attrs={'rows':1, 'cols':45}),
                'banch': forms.Textarea(attrs={'rows':1, 'cols':10}),
            	}

