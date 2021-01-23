from django.shortcuts import render
from django.urls import reverse
from .models import TfcCode
from .forms import CodeForm
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
 
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


    #def get_form(self):
        #form = super(CodeUpdate, self).get_form()
        #form.initial['id'] = TfcCode.objects.last().pk
        #form.fields['item'] = 'アイテム'
        #form.fields['description'].label = '詳細'
        #form.fields['remarks'].label = '備考'
        #form.fields['unit'].label = '単位'
        #form.fields['uprice'].label = '単価'
        #form.fields['ouritem'].label = 'ouritem'
        #form.fields['vol'].label = '容積'
        #form.fields['zaiko'].label = '在庫管理'
        #form.fields['kento'].label = '発注管理'
        #form.fields['hcode'].label = 'フクラ品番'
        #form.fields['cat'].label = '分類'
        #return form
