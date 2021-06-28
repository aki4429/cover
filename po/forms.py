from django import forms
from .models import TfcCode, Juchu, Condition, Po, Poline, Cart, Inv, Invline, Kento
from bootstrap_datepicker_plus import DatePickerInput
from django.core.validators import FileExtensionValidator
from django.core.files.storage import default_storage
from django.contrib.admin.widgets import AdminDateWidget

PO_ORDER = (
        ('pon', 'PO No.'),
        ('etd', 'ETD'),
        ('delivery', '納入指定日'),
        )


class CodeForm(forms.ModelForm):

    class Meta:
        model = TfcCode
        fields = [ 'hinban',
                    'item',
                    'description',
                    'remarks',
                    'unit',
                    'uprice',
                    #'ouritem',
                    'vol',
                    'zaiko',
                    'kento',
                    'hcode',
                    'cat' ]

        ### 追加 ###
        widgets = {
            'hinban': forms.Textarea(attrs={'rows':1, 'cols':15}),
            'item': forms.Textarea(attrs={'rows':1, 'cols':15}),
            'description': forms.Textarea(attrs={'rows':1, 'cols':15}),
            'remarks': forms.Textarea(attrs={'rows':1, 'cols':15}),
            'uprice': forms.Textarea(attrs={'rows':1, 'cols':5}),
            'vol': forms.Textarea(attrs={'rows':1, 'cols':5}),
            'hcode': forms.Textarea(attrs={'rows':1, 'cols':15}),
            'cat': forms.Textarea(attrs={'rows':1, 'cols':10}),
        }

class JuchuForm(forms.ModelForm):
    class Meta:
        model = Juchu
        fields = ('file_name', )

class KentoForm(forms.ModelForm):
    class Meta:
        model = Kento
        fields = ('file_name', )

class ConditionForm(forms.ModelForm):
    class Meta:
        model = Condition
        fields = [ 'name',
                    'shipment_per',
                    'shipto_1',
                    'shipto_2',
                    'shipto_3',
                    'shipto_4',
                    'shipto_5',
                    'via',
                    'forwarder',
                    'trade_term',
                    'payment_term',
                    'insurance',
                    'comment', 
                    'nic', ]

class DateInput(forms.DateInput):
    input_type = 'date'

class PoForm(forms.ModelForm):
    class Meta:
        model = Po
        fields = [
                'pod',
                'pon',
                'per',
                'port',
                'shipto',
                'etd',
                'comment',
                'delivery',
                'condition',
                'ft40',
                'ft20',
                ]
        widgets = {
                'pod':forms.DateInput(attrs={"type":"date"}),
                #'pod': DatePickerInput(
                #    format='%Y-%m-%d',
                #    options={
                #        'locale': 'ja',
                #        'dayViewHeaderFormat': 'YYYY年 MMMM',
                #    }
                #),
                'etd':forms.DateInput(attrs={"type":"date"}),
                'delivery':forms.DateInput(attrs={"type":"date"}),
                'pon': forms.Textarea(attrs={'rows':1, 'cols':15}),
                'per': forms.Textarea(attrs={'rows':1, 'cols':15}),
                'port': forms.Textarea(attrs={'rows':1, 'cols':15}),
                'shipto': forms.Textarea(attrs={'rows':1, 'cols':50}),
                'comment': forms.Textarea(attrs={'rows':1, 'cols':20}),
                #'ft40': forms.Textarea(attrs={'rows':1, 'cols':15}),
                #'ft20': forms.Textarea(attrs={'rows':1, 'cols':15}),
            }

class PolineForm(forms.ModelForm):
    class Meta:
        model = Poline
        fields = [
                #'code',
                'remark',
                'om',
                'qty',
                'balance',
                'po',
                'ocode',
                'hinmei',
                'kikaku',
                'set',
                ]
        ### 追加 ###
        widgets = {
            'remark': forms.Textarea(attrs={'rows':1, 'cols':15}),
            'ocode': forms.Textarea(attrs={'rows':1, 'cols':15}),
            'hinmei': forms.Textarea(attrs={'rows':1, 'cols':15}),
            'kikaku': forms.Textarea(attrs={'rows':1, 'cols':15}),
            'om': forms.Textarea(attrs={'rows':1, 'cols':15}),
            'qty': forms.Textarea(attrs={'rows':1, 'cols':5}),
        }

class CartForm(forms.ModelForm):
    class Meta:
        model = Cart
        fields = [
                'hinban',
                'juchubi',
                #'noki',
                'om',
                'qty',
                'flag',
                'code',
                'obic',
                ]
        ### 追加 ###
        widgets = {
            'juchubi':forms.DateInput(attrs={"type":"date"}),
            'hinban': forms.Textarea(attrs={'rows':1, 'cols':15}),
            'obic': forms.Textarea(attrs={'rows':1, 'cols':15}),
            'om': forms.Textarea(attrs={'rows':1, 'cols':15}),
            'flag': forms.Textarea(attrs={'rows':1, 'cols':15}),
            'qty': forms.Textarea(attrs={'rows':1, 'cols':5}),
            }

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

class InvForm(forms.ModelForm):
    class Meta:
        model = Inv
        fields = [
                'invn',
                'etd',
                'delivery',
                ]
        widgets = {
                'invn': forms.Textarea(attrs={'rows':1, 'cols':15}),
                #'etd': AdminDateWidget(),
                'etd':forms.DateInput(attrs={"type":"date"}),
                #'etd': DatePickerInput(
                #format='%Y-%m-%d',
                #options={
                #     'locale': 'ja',
                #     'dayViewHeaderFormat': 'YYYY年 MMMM',
                #}
            	#),
                #'delivery':AdminDateWidget(), 
                'delivery':forms.DateInput(attrs={"type":"date"}),
            	}


class InvlineForm(forms.ModelForm):
    class Meta:
        model = Invline
        fields = [
                'item',
                'qty',
                'minashi',
                'code',
                'inv',
                'poline',
                ]
        ### 追加 ###
        widgets = {
            'item': forms.Textarea(attrs={'rows':1, 'cols':15}),
            'qty': forms.Textarea(attrs={'rows':1, 'cols':5}),
            'minashi': forms.Textarea(attrs={'rows':1, 'cols':5}),
        }

class MakezaikoForm(forms.Form):
    begin_date = forms.DateField(label='取込開始日', \
            widget = forms.DateInput(attrs={"type":"date"}))


class SokoUpForm(forms.Form):
    sokof = forms.FileField(label='倉庫別在庫表',
        validators=[FileExtensionValidator(['csv' ])],
        #拡張子バリデーター。アップロードファイルの拡張子が違う時にエラー
        )

    def save(self):
        upload_file = self.cleaned_data['sokof']
        file_name = default_storage.save(upload_file.name, upload_file)
        #file属性で返す。
        return default_storage.open(file_name), default_storage.url(file_name)

class PoListForm(forms.Form):
    po_sort = forms.ChoiceField(
        label='ソート',
        widget = forms.RadioSelect,
        choices = PO_ORDER,
        required=True,
    )
