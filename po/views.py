from django.shortcuts import render
from loc.models import TfcCode
from django.views.generic import ListView
from django.db.models import Q
 
class CodeList(ListView):
    context_object_name = 'codes'
    model = TfcCode
    paginate_by = 10

    def get_queryset(self):
        q_word = self.request.GET.get('query')
        if q_word:
            codes = TfcCode.objects.filter(
                Q(item__icontains=q_word) | Q(description__icontains=q_word))
        else:
            codes = TfcCode.objects.all()
        return codes
