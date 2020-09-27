from django.shortcuts import render, get_object_or_404, redirect
from .forms import LocForm, ShijiForm, LocStatusForm
from .models import Locdata, Shiji, Seisan, LocStatus, Pick, Kakutei
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from .read_shiji import read_shiji

@login_required
def loc_list(request):
    ls = LocStatus.objects.all() 
    if len(ls) == 0 or ls[0].koshinbi == None :
        return redirect('status_edit')
    else:
        status = ls[0]
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
            'title':'カバー番地リスト',
            'koshinbi': status.koshinbi,
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
            shiji.shiji_date = shiji.file_name.name[11:19]
            shiji.save()
            return redirect('shiji_list')
    else:
        form = ShijiForm()
    return render(request, 'loc/model_form_upload.html', {
        'form': form
    })

@login_required
def shiji_list(request):
    shijis = Shiji.objects.order_by('-shiji_date')
    return render(request, 'loc/shiji_list.html', {'shijis': shijis})

@login_required
def shiji_del(request, shiji_id):
   shiji = get_object_or_404(Shiji, id=shiji_id)
   shiji.delete()
   return redirect('shiji_list')

@login_required
def seisan_list(request):
    ls = LocStatus.objects.all() 
    if len(ls) == 0 or ls[0].koshinbi == None :
        return redirect('status_edit')
    else:
        status = LocStatus.objects.get(id=1)
        koshinbi = status.koshinbi
        seisans = Seisan.objects.filter(seisan__gt=koshinbi).order_by('seisan')
    params = {
            'title':'生産リスト',
            'seisans':seisans,
            'status':status,
            }

    return render(request, 'loc/seisan_list.html', params)

@login_required
def make_seisan(request, shiji_id):
    Seisan.objects.all().delete()
    Pick.objects.all().delete()
    shiji = get_object_or_404(Shiji, id=shiji_id)

    #製造指示日を記録
    ls = LocStatus.objects.all() 
    if len(ls) == 0 or ls[0].koshinbi == None :
        return redirect('status_edit')
    status = LocStatus.objects.get(pk=1)
    status.shijibi = shiji.shiji_date
    status.save()

    shiji_file_name =  shiji.file_name.path
    sdata = read_shiji(shiji_file_name)

    add_seisan = []
    for row in sdata:
        seisan = Seisan(code = row[0], \
                om = row[1], seisan = row[2], qty = row[3])
        add_seisan.append(seisan)

    Seisan.objects.bulk_create(add_seisan) 

    locs = list(Locdata.objects.order_by('banch').values())
    koshinbi = LocStatus.objects.get(pk=1).koshinbi
    if koshinbi == None:
        return redirect('status_edit')
    else:
        seis = list(Seisan.objects.filter(seisan__gt=koshinbi).order_by('seisan').values())

    picks = pickup(seis, locs)

    add_pick =[]
    for row in picks:
        pick = Pick(code = row[0], qty = row[1], loc_qty = row[2],
                seisan = row[3], om = row[4], banch = row[5])
        add_pick.append(pick)

    Pick.objects.bulk_create(add_pick) 

    return redirect('pick_list')

from .pickup import pickup
@login_required
def make_pick(request):
    Pick.objects.all().delete()
    locs = list(Locdata.objects.order_by('banch').values())
    ls = LocStatus.objects.all() 
    if len(ls) == 0 or ls[0].koshinbi == None :
        return redirect('status_edit')
    else:
        koshinbi = ls[0].koshinbi
        seis = list(Seisan.objects.filter(seisan__gt=koshinbi).order_by('seisan').values())

    picks = pickup(seis, locs)

    add_pick =[]
    for row in picks:
        pick = Pick(code = row[0], qty = row[1], loc_qty = row[2],
                seisan = row[3], om = row[4], banch = row[5])
        add_pick.append(pick)

    Pick.objects.bulk_create(add_pick) 

    return redirect('pick_list')

@login_required
def pick_list(request):
    picks = Pick.objects.order_by('seisan', 'banch')
    ls = LocStatus.objects.all() 
    if len(ls) == 0 or ls[0].koshinbi == None :
        return redirect('status_edit')
    else:
        status = ls[0]

    if len(Kakutei.objects.all()) == 0:
        k = Kakutei()
        k.save()
    kaku = Kakutei.objects.last()
    params = {
            'kaku':kaku,
            'pick':picks[0],
            'picks':picks,
            'status':status,
            }
    return render(request, 'loc/pick_list.html', params)

@login_required
def koshin(request, pick_id ):
    #pick_id はpicks[0]のidが与えられます。
    #seisanbiが該当するpickデータの数量を番地リストから差し引きます。
    #更新したpickデータをkakuteiデータに残します。
    last_pick = get_object_or_404(Pick, id=pick_id)
    seisanbi = last_pick.seisan
    add_kaku = []
    picks = Pick.objects.filter(seisan = seisanbi)
    for pick in picks:
        if pick.banch != 'mitei':
            loc = Locdata.objects.get(banch = pick.banch)
            loc.qty = loc.qty - pick.qty
            if loc.qty == 0:
                loc.code = 'empty'
            loc.save()

            kaku = Kakutei()
            kaku.code = pick.code
            kaku.qty = pick.qty
            kaku.seisan = pick.seisan
            kaku.om = pick.om
            kaku.banch = pick.banch
            add_kaku.append(kaku)
            
    Kakutei.objects.bulk_create(add_kaku)

    status = LocStatus.objects.get(id=1)
    status.koshinbi = seisanbi
    status.save()
    return redirect('make_pick')

def rollback(request, kaku_id):
    #kakutei_id はkakus.lastのidが与えられます。
    #seisanbiが該当するpickデータの数量を番地リストから差し引きます。
    #更新したpickデータをkakuteiデータに残します。
    last_kaku = get_object_or_404(Kakutei, id=kaku_id)
    seisanbi = last_kaku.seisan
    mess = ""
    kakus = Kakutei.objects.filter(seisan = seisanbi)
    for kaku in kakus:
        loc = Locdata.objects.get(banch = kaku.banch)
        if loc.code == 'empty':
            loc.code = kaku.code
        if loc.code != kaku.code :
            mess = "ピック指示{0}は該当する番地内容が違います。".format(kaku)
        else:
            loc.qty = loc.qty + kaku.qty
            loc.save()

    Kakutei.objects.filter(seisan = seisanbi).delete()

    status = LocStatus.objects.get(id=1)
    status.koshinbi = Kakutei.objects.last().seisan
    status.save()

    return redirect('make_pick')

@login_required
def status_edit(request):
    if len(LocStatus.objects.all()) == 0:
        status = LocStatus(id=1)
    else: 
        status = LocStatus.objects.get(id=1)
    if request.method == "POST":
        form = LocStatusForm(request.POST, instance=status)
        if form.is_valid():
            loc = form.save()
            return render(request, 'loc/status_detail.html', {'status': status})

    form = LocStatusForm(request.POST, instance=status)
    return render(request, 'loc/status_new.html', {'form': form})
