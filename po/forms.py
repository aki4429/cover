from django import forms
from .models import TfcCode


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
