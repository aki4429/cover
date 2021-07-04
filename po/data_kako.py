#!/usr/bin/env python
# -*- coding: utf-8 -*-

# juchu_read のデータを受け取って、CH232, 271, 907などは、
# セットのクッションを減らし、LH03は、脚オーダーを追加する
# ための関数
#juchu_read のデータは cart のリスト
#Cart オブジェクトの配列：(例)
#CH271E-49 SP/223 JUC000026284 3 CH271   0001877 ﾏﾁﾙﾀﾞ ｶｳﾁ 
#CH271   SE 49       DB  SP/223        Z 0
#cart.hinban, cart.om, cart.juhcubi, cart.noki, cart.qty, cart.obic, 
#cart.hinmei, cart.kikaku, cart.set)

#271の場合の処理
#(1)セット品にするべき37の個数と品番、om 番号をリストにする。
#(2) データを走査し、該当するセット品37を見つけ、必要数セットフラグを立てる

#品番を受けてCH271の製品コードで37付きモデルだったら、
#セットになる37コードとセット数量, om番号を返す。

from po.models import Cart, TfcCode
import copy

def check_271(cart):
    if 'CH271' in cart.hinban.split('-')[0]:
        if '-03 ' in cart.hinban:
            cu = 'CH271-37 ' + cart.hinban.split(' ')[1]
            return [cu, int(float(cart.qty)) * 2, cart.om]
        elif '-08 ' in cart.hinban \
            or '-09 ' in cart.hinban \
            or '-41 ' in cart.hinban \
            or '-42 ' in cart.hinban \
            or '-49 ' in cart.hinban \
            or '-50 ' in cart.hinban :
            cu = 'CH271-37 ' + cart.hinban.split(' ')[1]
            return [cu, int(float(cart.qty)) * 1, cart.om]
        else:
            return []

    else:
        return []

def check_232(cart):
    if 'CH232' in cart.hinban.split('-')[0]:
        if '-03 ' in cart.hinban:
            cu = 'CH232W-37 ' + cart.hinban.split(' ')[1]
            return [cu, int(float(cart.qty)) * 2, cart.om]
        elif '-06 ' in cart.hinban \
            or '-07 ' in cart.hinban \
            or '-08 ' in cart.hinban \
            or '-09 ' in cart.hinban \
            or '-20N ' in cart.hinban \
            or '-49 ' in cart.hinban \
            or '-50 ' in cart.hinban :
            cu = 'CH232W-37 ' + cart.hinban.split(' ')[1]
            return [cu, int(float(cart.qty)) * 1, cart.om]
        else:
            return []

    else:
        return []

def check_lh(cart):
    if 'LH03' in cart.hinban.split('-')[0]:
        #カバーは除く
        if 'C ' not in cart.hinban:
            #スツールはLEG=Sx1がつく
            if "-17 " in cart.hinban or \
                    "-17L " in cart.hinban:
                leg = 'LH03LEG-S'
                return [leg, int(float(cart.qty)) * 1, cart.om]
            #それ以外は、LEG-Lx1
            else:
                leg = 'LH03LEG-L'
                return [leg, int(float(cart.qty)) * 1, cart.om]
        else:
            return []
    else:
        return []

#加算リストをバラバラと作らないために合算する関数
def plus_if_exist(add_list, cu_list):
    for row in add_list:
        #コードとom番号が同じの場合、数量を加算
        if row[0] == cu_list[0] and row[2] == cu_list[2] :
            row[1] += cu_list[1]
            return add_list
    #同じものがなければ、レコードを追加
    return add_list.append(cu_list)

#cartリストから、セットCUのリストを作る
def add_cu(data):
    add_list = [] #品番, 数量,om
    for cart in data:
        cu_list = check_271(cart) 
        if len(cu_list) > 0 :
            plus_if_exist(add_list, cu_list)
        cu_list = check_232(cart) 
        if len(cu_list) > 0 :
            plus_if_exist(add_list, cu_list)

    return add_list

#cartリストから、LH-LEGの追加リストを作る
def add_leg(data):
    add_list = [] #品番, 数量,om
    for cart in data:
        leg_list = check_lh(cart) 
        if len(leg_list) > 0 :
            plus_if_exist(add_list, leg_list)

    return add_list

#受注データにセットクッションがあれば、setflag項目をセット
def make_set(data):
    add_list = add_cu(data)
    for row in add_list: #品番,数量, om
        #print('row', row)
        counter = row[1] #数量をセット
        while(counter != 0): #counterゼロになるまで繰り返し
            for cart in data:
                #addlist のcuコードを見つけたら、setflagを1にする。
                if row[0] == cart.hinban and row[2] == cart.om and\
                        cart.setflag == 0 and counter != 0:
                    if cart.qty == counter:
                        cart.setflag = 1
                        counter = 0
                    elif cart.qty <  counter : #数量がcounter より小さい時
                        cart.setflag = 1
                        counter = counter - cart.qty #セットして、数量分減
                    elif cart.qty >  counter : #数量がcounterより大きい
                        cart_new = copy.deepcopy(cart)
                        cart_new.qty = counter #数量=カウンターの新cart作成
                        cart_new.setflag = 1 #setは1
                        data.append(cart_new)
                        cart.qty = cart.qty - counter #残りの数量はset=0のまま
                        counter = 0

    return data

#受注データにLH leg を追加
def make_leg(data):
    add_list = add_leg(data)
    for row in add_list: #品番,数量, om
        cart = Cart(hinban=row[0], qty=row[1], om = row[2], setflag=-1)
        data.append(cart)

    return data

#TfcCodeがあればflag=ok, なければ, no, 複数は Double
def check_code(data):
    for cart in data:
        results = TfcCode.objects.filter(hinban = cart.hinban)
        if len(results) == 0:
            cart.flag = 'NO'
        elif len(results) == 1:
            cart.flag = 'ok'
            cart.code = results.first()
        elif len(results) > 1:
            cart.flag = 'Double'

    return data

def show_data(data):
    for cart in data:
        print('type', type(cart) )
        print(cart.hinban, cart.om, cart.juhcubi, cart.noki, cart.qty, cart.obic, cart.hinmei, cart.kikaku, cart.setflag)

#以下は過去のコード、今は使用していない
"""
#条件によってデータ追加する。
def kako_add(data):
    new_list =[]
    for row in data:
        new_list.append(row)
        if "CH907-06 " in row[0]:
            new_list.append([row[0].replace("CH907-06", "CH907-35"),
                row[1], row[2], row[3], row[4] * -1])
            new_list.append([row[0].replace("CH907-06", "CH907-37"),
                row[1], row[2], row[3], row[4] * -1])

        if "CH907-07 " in row[0]:
            new_list.append([row[0].replace("CH907-07", "CH907-35"),
                row[1], row[2], row[3], row[4] * -1])
            new_list.append([row[0].replace("CH907-07", "CH907-37"),
                row[1], row[2], row[3], row[4] * -1])

        if "CH907-49 " in row[0]:
            new_list.append([row[0].replace("CH907-49", "CH907-35"),
                row[1], row[2], row[3], row[4] * -1])
            new_list.append([row[0].replace("CH907-49", "CH907-37"),
                row[1], row[2], row[3], row[4] * -1])

        if "CH907-50 " in row[0]:
            new_list.append([row[0].replace("CH907-50", "CH907-35"),
                row[1], row[2], row[3], row[4] * -1])
            new_list.append([row[0].replace("CH907-50", "CH907-37"),
                row[1], row[2], row[3], row[4] * -1])

        #CH907でコンビ布地の指定がない場合、おなじ布地名をコンビ名と
        #して追加。(ダブルでコードを選ばないように
        #ただし、35/37はそのまま。
        #if "CH907" in row[0]:
        #    if "CH907-35" not in row[0] and "CH907-37" not in row[0] and \
        #     "C " not in row[0]: 
        #        if len(row[0].split(" ")) < 3:
        #            row[0] = row[0] + " " + row[0].split(" ")[1]

        #CH261は、03を03+17コードに変換して、17をマイナス。
        #セットで注文くる前提の処理
        if "CH261-03 " in row[0]:
            new_list.append([row[0].replace("CH261-03", "CH261-17"),
                row[1], row[2], row[3], row[4] * -1])
            row[0] = row[0].replace("CH261-03", "CH261-03+17")

    return new_list

#品目CD row[0] と 受注# row[1] が同じならば、数量row[4]を加算
def sum(data):
    #品番順受注番号順に並べ替え
    #data = sorted(data, key = lambda x:x[0])
    data = sorted(data, key = lambda x:x[1])
    #コードrow[0]+ 受注番号row[1] の辞書を作る
    new_dic = {}
    for row in data:
        #コードrow[0]+ 受注番号row[1] の組み合わせが辞書にあれば
        #データの数量を加算
        if row[0]+row[1] in new_dic:
            new_dic[row[0]+row[1]][4] += row[4]
        #無ければ、辞書にデータを登録
        else:
            new_dic[row[0]+row[1]] = row

    #辞書の値の取り出し。
    new_data =[]
    new_data = new_dic.values()

    del_list = []
    #数量0のデータを除外
    for row in new_data:
        if row[4] != 0:
            del_list.append(row)

    return del_list

def check(data, codes):
    new_data = []
    for row in data:
        flag="NO"
        idn=""
        for code in codes:
            #if row[0] in code[1] :
            if row[0] == code[1] :
                #print('row[0]', row[0])
                #print('code[1]', code[0], code[1])
                if flag == "NO":
                    flag = "ok"
                    idn = code[0]
                else:
                    flag = "Double"

        #obic_code を末尾に持っていきたいので、取り出しておく
        if len(row) > 5 :  #obic_code がある場合、データ帳は６になる。
            obic_code = row.pop()
        else:
            obic_code =''

        row.append(flag)
        row.append(idn)
        row.append(obic_code)


    return data

"""
