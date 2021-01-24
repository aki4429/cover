from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from .models import TfcCode, Juchu
from .forms import CodeForm, JuchuForm
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from django.contrib.auth.decorators import login_required
 
class CodeList(LoginRequiredMixin, ListView):
    context_object_name = 'codes'
    model = TfcCode

    #paginate_by = 10
    #検索語とフィールド名を指定して、その言葉がフィールドに
    #含まれるクエリーセットを返す関数。
    #検索語はスペースで区切って、リストでANDでつなげる
    def make_q(self,query, q_word, f_word):
        #(2)キーワードをリスト化させる(複数指定の場合に対応させるため)
        search      = self.request.GET[q_word].replace("　"," ")
        search_list = search.split(" ")
        filter = f_word + '__' + 'contains' #name__containsを作る
        #(例)info=members.filter(**{ filter: search_string })
        #(3)クエリを作る
        for word in search_list:
        #TIPS:AND検索の場合は&を、OR検索の場合は|を使用する。
            query &= Q(**{ filter: word })
            #(4)作ったクエリを返す
        return query


    def get_queryset(self):
        query = Q()
        flag = 0 #一つも検索語がなければ、flag==0
        if 'qh' in self.request.GET:
            query = self.make_q(query, 'qh', 'hinban')
            flag += 1

        if 'qi' in self.request.GET:
            query = self.make_q(query, 'qi', 'item')
            flag += 1

        if 'qs' in self.request.GET:
            query = self.make_q(query, 'qs', 'description')
            flag += 1

        if 'qb' in self.request.GET:
            query = self.make_q(query, 'qb', 'remarks')
            flag += 1

        if 'qc' in self.request.GET:
            query = self.make_q(query, 'qc', 'hcode')
            flag += 1

        if 'qt' in self.request.GET:
            query = self.make_q(query, 'qt', 'cat')
            flag += 1

        if 'z' in self.request.GET:
            query = self.make_q(query, 'z', 'zaiko')
            flag += 1

        if 'h' in self.request.GET:
            query = self.make_q(query, 'h', 'kento')
            flag += 1

        if flag == 0:
            codes = TfcCode.objects.order_by('hinban')
        else:
            print('Query',query)
            codes = TfcCode.objects.filter(query).order_by('hinban')

        return codes

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title']='TFCコードリスト'
        return context


class CodeCopy(LoginRequiredMixin, UpdateView):
    template_name = 'po/code_update.html'
    model = TfcCode
    form_class = CodeForm

    def get_success_url(self):
        return reverse('tfc_code')

    #ここでコピーするためにget_objectをオーバーライドします。
    def get_object(self, queryset=None):
        #self.request.GETは使えないので、self.kwargsを使うところがミソ
        tfccode = TfcCode.objects.get(pk=self.kwargs.get('pk'))
        #プライマリーキーを最新に。これがしたいためのオーバーライド
        tfccode.pk = TfcCode.objects.last().pk + 1
        return tfccode

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title']='TFCコードコピー'
        #context['last_id'] = TfcCode.objects.last().pk
        return context

class CodeUpdate(LoginRequiredMixin, UpdateView):
    template_name = 'po/code_update.html'
    model = TfcCode
    form_class = CodeForm

    def get_success_url(self):
        return reverse('tfc_code')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title']='TFCコード編集'
        #context['last_id'] = TfcCode.objects.last().pk
        return context

class CodeDelete(LoginRequiredMixin, DeleteView):
    template_name = 'po/code_confirm_delete.html'
    model = TfcCode
    form_class = CodeForm

    def get_success_url(self):
        return reverse('tfc_code')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title']='TFCコード削除確認'
        return context

class CodeDetail(LoginRequiredMixin, DetailView):
    template_name = 'po/code_detail.html'
    model = TfcCode

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title']='TFCコード詳細'
        return context

class CodeCreate(LoginRequiredMixin, CreateView):
    template_name = 'po/code_create.html'
    model = TfcCode
    form_class = CodeForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title']='TFCコード作成'
        return context

@login_required
def juchu_upload(request):
    if request.method == 'POST':
        form = JuchuForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('juchu_list')
    else:
        form = JuchuForm()

    context = {
        'title' : '受注データアップロード',
        'form': form
        }

    return render(request, 'po/juchu_upload.html', context )
    
 
class JuchuList(LoginRequiredMixin, ListView):
    context_object_name = 'juchus'
    template_name = 'po/juchu_list.html'
    model = Juchu
    form_class = JuchuForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title']='受注データリスト'
        return context


@login_required
def juchu_delete(request, pk):
   juchu = get_object_or_404(Juchu, id=pk)
   juchu.delete()
   return redirect('juchu_list')

