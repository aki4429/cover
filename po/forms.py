from django import forms
from .models import TfcCode, Juchu, Condition, Po, Poline, Cart
from bootstrap_datepicker_plus import DatePickerInput


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
                'delivery',
                'condition',
                'ft40',
                'ft20',
                ]
        widgets = {
                'pod': DatePickerInput(
                    format='%Y-%m-%d',
                    options={
                        'locale': 'ja',
                        'dayViewHeaderFormat': 'YYYY年 MMMM',
                    }
                ),
                'etd': DatePickerInput(
                    format='%Y-%m-%d',
                    options={
                        'locale': 'ja',
                        'dayViewHeaderFormat': 'YYYY年 MMMM',
                    }
                ),
                'delivery': DatePickerInput(
                    format='%Y-%m-%d',
                    options={
                        'locale': 'ja',
                        'dayViewHeaderFormat': 'YYYY年 MMMM',
                    }
                ),
                'pon': forms.Textarea(attrs={'rows':1, 'cols':15}),
                'per': forms.Textarea(attrs={'rows':1, 'cols':15}),
                'port': forms.Textarea(attrs={'rows':1, 'cols':15}),
                'shipto': forms.Textarea(attrs={'rows':1, 'cols':50}),
                'shipto': forms.Textarea(attrs={'rows':1, 'cols':50}),
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
                ]
        ### 追加 ###
        widgets = {
            'remark': forms.Textarea(attrs={'rows':1, 'cols':15}),
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
                'juchubi': DatePickerInput(
                    format='%Y-%m-%d',
                    options={
                        'locale': 'ja',
                        'dayViewHeaderFormat': 'YYYY年 MMMM',
                    }
                ),
            'hinban': forms.Textarea(attrs={'rows':1, 'cols':15}),
            'obic': forms.Textarea(attrs={'rows':1, 'cols':15}),
            'om': forms.Textarea(attrs={'rows':1, 'cols':15}),
            'flag': forms.Textarea(attrs={'rows':1, 'cols':15}),
            'qty': forms.Textarea(attrs={'rows':1, 'cols':5}),
            }
