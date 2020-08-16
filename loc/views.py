from django.shortcuts import render
from .models import Locdata
from django.shortcuts import render, get_object_or_404

def loc_list(request):
    locs = Locdata.objects.filter(qty__gt=0 ).order_by('banch')
    return render(request, 'loc/loc_list.html', {'locs': locs})

def loc_detail(request, pk):
    loc = get_object_or_404(Locdata, pk=pk)
    return render(request, 'loc/loc_detail.html', {'loc': loc})

