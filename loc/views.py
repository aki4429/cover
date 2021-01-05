from django.shortcuts import render, get_object_or_404, redirect
from .forms import LocForm, ShijiForm, LocStatusForm, OrderChoiceForm, ChoiceForm, InvUpForm
from .models import Locdata, Shiji, Seisan, LocStatus, Pick, Kakutei, Addcover
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from .read_shiji import read_shiji
from .drop  import drop
from django.conf import settings
import xlrd
from .read_inv import pick_items
from django.http import HttpResponse
import io
import csv
import os
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse
from .input_case import make_input_list


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
    
    #LocStatusにデータがないときはstatus_editに飛ばして、
    #更新日を設定してもらいます。
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
    
    #LocStatusにデータがないときはstatus_editに飛ばして、
    #更新日を設定してもらいます。
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
    
    #LocStatusにデータがないときはstatus_editに飛ばして、
    #更新日を設定してもらいます。
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
    choice1 = 'banch'
    if request.method == 'POST' and 'choice1' in request.POST:
        choice1 = request.POST['choice1']
        #picks = Pick.objects.order_by('seisan', choice1)
    elif request.method == 'POST' and 'seisan' in request.POST:
        seisan = request.POST['seisan']
        #down_pick(seisan)
        picks = Pick.objects.filter(seisan=seisan).order_by('seisan', choice1)
        #download_pick(request,picks)
        #write_pick(picks)
    else:
        picks = Pick.objects.order_by('seisan', choice1)
    
    #LocStatusにデータがないときはstatus_editに飛ばして、
    #更新日を設定してもらいます。
    ls = LocStatus.objects.all() 
    if len(ls) == 0 or ls[0].koshinbi == None :
        return redirect('status_edit')
    else:
        status = ls[0]

    if len(Kakutei.objects.all()) == 0:
        k = Kakutei()
        k.save()
    kaku = Kakutei.objects.last()

    bq_word = request.GET.get('banchquery')
    cq_word = request.GET.get('codequery')
    c2q_word = request.GET.get('code2query')
    bq_clear = request.GET.get('bqclear')

    if not bq_word :
        bq_word = ''
    if not cq_word :
        cq_word = ''
    if not c2q_word :
        c2q_word = ''

    if cq_word == '' and bq_word != '':
        picks = Pick.objects.filter(
            Q(banch__icontains=bq_word ), 
            Q(code__icontains=cq_word), 
            Q(code__icontains=c2q_word)).order_by('banch')
    elif bq_word == '' and cq_word != '' :
        picks = Pick.objects.filter(
            Q(banch__icontains=bq_word ), 
            Q(code__icontains=cq_word), 
            Q(code__icontains=c2q_word)).order_by('code')

    #result =[]
    #i=0
    #seisans = Pick.objects.all().values('seisan')
    #for seisan in seisans:
    #    #dates.append(seisan['seisan'])
    #    #dates = sorted(list(set(dates)))
    #    for d in dates:
    #        result.append([i+1, d])
    #        i += 1


    cform = OrderChoiceForm()
    pform = ChoiceForm()
    params = {
            'cform':cform,
            'pform':pform,
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

    locs = Locdata.objects.all()
    locs = drop(locs)
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
        upper = Locdata.objects.get(banch = kaku.banch.replace('2', '1').replace('4', '3'))
        if loc.code == 'empty':
            loc.code = kaku.code
        if loc.code != kaku.code :
            #該当番地の箱の内容が違うが、上の箱が空の場合、
            #空の箱に入れて、上下入れ替え
            if upper.code == 'empty' :
                upper.code = kaku.code
                upper.qty = kaku.qty
                loc.banch = upper.banch
                upper.banch = kaku.banch
                upper.save()
                loc.save()
            else:
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
        form = LocStatusForm(request.POST, instance=status)
        if form.is_valid():
            loc = form.save()
            return render(request, 'loc/status_detail.html', {'status': status})

    form = LocStatusForm(request.POST, instance=status)
    return render(request, 'loc/status_new.html', {'form': form})

#@login_required
#def down_pick(request, pick_id):
#    pick = Pick.objects.get(id=pick_id)
#    download_pick(pick.seisan)
#return redirect('pick_list')

from .s2d import d2sh
@login_required
def download_pick(request, pick_pk):
    pick = get_object_or_404(Pick, pk=pick_pk)
    picks = Pick.objects.filter(seisan = pick.seisan).order_by('banch', 'code' )
    output = io.StringIO()
    writer = csv.writer(output)
    lines =[]
    lines.append(['番地','コード', 'ピック数量', '番地在庫', '生産日', '受注NO'])
    for pick in picks:
        lines.append([pick.banch, pick.code, pick.qty, pick.loc_qty, 
                d2sh(pick.seisan), pick.om])
    writer.writerows(lines)
    response = HttpResponse(output.getvalue(), content_type="text/csv", charset = "ShiftJIS")
    response["Content-Disposition"] = "filename=pick.csv"
    return response

def write_pick(picks):
    path = 'shiji.csv'
    filename = os.path.join(settings.MEDIA_ROOT, path)
    lines = []
    lines.append(['番地','コード', 'ピック数量', '番地在庫', '生産日', '受注NO'])
    with open(filename, 'w', encoding='CP932') as f:
        writer = csv.writer(f)
        for pick in picks:
            lines.append([pick.banch, pick.code, pick.qty, pick.loc_qty, 
                d2sh(pick.seisan), pick.om])
        writer.writerows(lines)

@login_required
def kaku_list(request):
    
    #LocStatusにデータがないときはstatus_editに飛ばして、
    #更新日を設定してもらいます。
    ls = LocStatus.objects.all() 
    if len(ls) == 0 or ls[0].koshinbi == None :
        return redirect('status_edit')
    else:
        status = ls[0]

    koshinbi = status.koshinbi

    if len(Kakutei.objects.all()) == 0:
        k = Kakutei()
        k.save()

    kakus = Kakutei.objects.filter(seisan__gt=koshinbi).order_by('seisan', 'banch')


    params = {
            'title':'確定指示リスト',
            'koshinbi': status.koshinbi,
            'kakus':kakus,
            }
    return render(request, 'loc/kaku_list.html', params)


@login_required
def upload_inv(request):
    INVN = (2,0) #inv.#位置
    form = InvUpForm()
    #template_name = 'inv/upload_inv.html'

    if request.method == 'POST':
        form = InvUpForm(request.POST, request.FILES)  # Do not forget to add: request.FILES
        if form.is_valid():
            #前の内容は全削除する。
            Addcover.objects.all().delete()
            # Do something with our files or simply save them
            # if saved, our files would be located in media/ folder under the project's base folder
            file, download_url = form.save()
            #book = xlrd.open_workbook(file.name)
            dict, invn = pick_items(file.name)
            adds = []
            for key, val in dict.items():
                addcover = Addcover(hcode = key, qty = val, invn = invn)
                adds.append( addcover)

            Addcover.objects.bulk_create(adds)
            addcovers = Addcover.objects.all()

            context = {
                #'download_url': download_url,
                #'dict' : dict,
                'addcovers' : addcovers,
                'invn': invn,
                'form': form,
                }
            os.remove(file.name)
            return render(request, 'loc/upload_inv.html', context)
    return render(request, 'loc/upload_inv.html', locals())

class AddcoverList(LoginRequiredMixin, ListView):
    context_object_name = 'addcovers'
    queryset = Addcover.objects.order_by('hcode')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title']='追加カバーリスト'
        invn = Addcover.objects.all()[0].invn
        context['invn']= invn
        return context

class AddcoverUpdate(LoginRequiredMixin, UpdateView):
    template_name = 'loc/adds_update.html'
    model = Addcover
    fields = ['hcode', 'qty', 'invn']
 
    def get_success_url(self):
        return reverse('adds_list')
 
    def get_form(self):
        form = super(AddcoverUpdate, self).get_form()
        form.fields['hcode'].label = 'コード'
        form.fields['qty'].label = '数量'
        form.fields['invn'].label = 'インボイスNo.'
        return form

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title']='入荷カバー編集'
        return context

class AddcoverCreate(LoginRequiredMixin, CreateView):
    #template_name = 'loc/addcover_form.html'
    model = Addcover
    fields = ['hcode', 'qty', 'invn']

    def get_success_url(self):
        return reverse('adds_list')

    def get_form(self):
        form = super(AddcoverCreate, self).get_form()
        form.fields['hcode'].label = 'コード'
        form.fields['qty'].label = '数量'
        form.initial['invn'] = Addcover.objects.first().invn
        return form

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title']='入荷カバー新規作成'
        return context

class AddcoverDelete(LoginRequiredMixin, DeleteView):
    #template_name = 'loc/addcover_confirm_delete.html'
    model = Addcover

    def get_success_url(self):
        return reverse('adds_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title']='入荷カバー削除確認'
        return context

def input_case(request):
    response = HttpResponse(content_type='text/csv; charset=Shift-JIS')
    response['Content-Disposition'] = 'attachment; filename="input_case.csv"'
    # HttpResponseオブジェクトはファイルっぽいオブジェクトなので、csv.writerにそのまま渡せます。
    input_cases = make_input_list(Locdata, Addcover)
    writer = csv.writer(response)
    writer.writerows(input_cases)
    response.write(sio.getvalue().encode('cp932'))
    return response
