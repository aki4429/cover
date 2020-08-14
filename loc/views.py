from django.shortcuts import render
from .models import Locdata

def loc_list(request):
    locs = Locdata.objects.filter(qty__gt=0 ).order_by('banch')
    return render(request, 'loc/loc_list.html', {'locs': locs})
