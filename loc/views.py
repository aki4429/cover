from django.shortcuts import render, get_object_or_404, redirect
from .forms import LocForm, ShijiForm
from .models import Locdata, Shiji
from django.db.models import Q
from django.contrib.auth.decorators import login_required

@login_required
def loc_list(request):
    bq_word = request.GET.get('banchquery')
    cq_word = request.GET.get('codequery')
    c2q_word = request.GET.get('code2query')
    bq_clear = request.GET.get('bqclear')

    if not bq_word :
        # セッションにデータがあればそれを使う
        if request.session.get('banchquery'):
            bq_word = request.session.get('banchquery')
            #ただし、クリアボタンで取り消し
            if bq_clear:
                del request.session['banchquery']
                bq_word = ''
        else:
            bq_word = ''
    else:
        # セッションにデータを格納
        request.session['banchquery'] = bq_word

    if not cq_word :
        cq_word = ''
    if not c2q_word :
        c2q_word = ''

    if cq_word == '':
        locs = Locdata.objects.filter(
            Q(banch__icontains=bq_word ), 
            Q(code__icontains=cq_word), 
            Q(code__icontains=c2q_word)).order_by('banch')
    else:
        locs = Locdata.objects.filter(
            Q(banch__icontains=bq_word ), 
            Q(code__icontains=cq_word), 
            Q(code__icontains=c2q_word)).order_by('code')

 
    #locs = Locdata.objects.filter(qty__gt=0 ).order_by('banch')
    #locs = Locdata.objects.order_by('banch')
    params = {
            'locs':locs,
            'bq_word':bq_word,
            }
    return render(request, 'loc/loc_list.html', params)

@login_required
def loc_detail(request, pk):
    loc = get_object_or_404(Locdata, pk=pk)
    return render(request, 'loc/loc_detail.html', {'loc': loc})

@login_required
def loc_new(request):
    if request.method == "POST":
        form = LocForm(request.POST)
        if form.is_valid():
            loc = form.save()
            return redirect('loc_detail', pk=loc.pk)
    else:
        form = LocForm()
    return render(request, 'loc/loc_new.html', {'form': form})

@login_required
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

@login_required
def loc_remove(request, pk):
    loc = get_object_or_404(Locdata, pk=pk)
    form = LocForm(instance=loc) #POSTデータが送られて来ないのでそのまま:request.POST引数はなし
    loc = form.save(commit=False)
    loc.code = "empty"
    loc.qty = "0"
    loc.save()
    return redirect('loc_detail', pk=loc.pk)

@login_required
def loc_del(request, pk):
    loc = get_object_or_404(Locdata, pk=pk)
    loc.delete()
    return redirect('loc_list')

@login_required
def model_form_upload(request):
    if request.method == 'POST':
        form = ShijiForm(request.POST, request.FILES)
        if form.is_valid():
            shiji = form.save(commit=False)
            shiji.shiji_date = shiji.file_name.name[10:20]
            shiji.save()
            shijis = Shiji.objects.all()
            return render(request, 'loc/shiji_list.html', {'shijis': shijis})
    else:
        form = ShijiForm()
    return render(request, 'loc/model_form_upload.html', {
        'form': form
    })

@login_required
def shiji_list(request):
    shijis = Shiji.objects.order_by('uploaded_at')
    return render(request, 'loc/shiji_list.html', {'shijis': shijis})
