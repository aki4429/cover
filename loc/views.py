from django.shortcuts import render, get_object_or_404, redirect
from .forms import LocForm
from .models import Locdata
from django.db.models import Q

def loc_list(request):
    bq_word = request.GET.get('banchquery')
    cq_word = request.GET.get('codequery')
    c2q_word = request.GET.get('code2query')

    if not bq_word :
        bq_word = ''
    if not cq_word :
        cq_word = ''
    if not c2q_word :
        c2q_word = ''

    locs = Locdata.objects.filter(
        Q(banch__icontains=bq_word ), 
        Q(code__icontains=cq_word), 
        Q(code__icontains=c2q_word)).order_by('banch')
 
    #locs = Locdata.objects.filter(qty__gt=0 ).order_by('banch')
    #locs = Locdata.objects.order_by('banch')
    return render(request, 'loc/loc_list.html', {'locs': locs})

def loc_detail(request, pk):
    loc = get_object_or_404(Locdata, pk=pk)
    return render(request, 'loc/loc_detail.html', {'loc': loc})

def loc_new(request):
    if request.method == "POST":
        form = LocForm(request.POST)
        if form.is_valid():
            loc = form.save()
            return redirect('loc_detail', pk=loc.pk)
    else:
        form = LocForm()
    return render(request, 'loc/loc_new.html', {'form': form})

def loc_edit(request, pk):
    loc = get_object_or_404(Locdata, pk=pk)
    if request.method == "POST":
        form = LocForm(request.POST, instance=loc)
        if form.is_valid():
            loc = form.save()
            return redirect('loc_detail', pk=loc.pk)
    else:
        form = LocForm(instance=loc)
    return render(request, 'loc/loc_new.html', {'form': form})

def loc_remove(request, pk):
    loc = get_object_or_404(Locdata, pk=pk)
    form = LocForm(instance=loc) #POSTデータが送られて来ないのでそのまま:request.POST引数はなし
    loc = form.save(commit=False)
    loc.code = "empty"
    loc.qty = "0"
    loc.save()
    return redirect('loc_detail', pk=loc.pk)

def loc_del(request, pk):
    loc = get_object_or_404(Locdata, pk=pk)
    loc.delete()
    return redirect('loc_list')