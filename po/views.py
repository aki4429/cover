from django.shortcuts import render
from loc.models import TfcCode
from django.views.generic import ListView
from django.db.models import Q
 
class CodeList(ListView):
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
            codes = TfcCode.objects.all()
        else:
            print('Query',query)
            codes = TfcCode.objects.filter(query)

        return codes
