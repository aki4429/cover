#!/usr/bin/env python3
# -*- coding: utf-8 -*-

CAT_ORDER = {'NEW':0, '布地':1,'ﾇｰﾄﾞ':2,'ｶﾊﾞｰ':3,'INCOON':4, 'INCOON BED':5, '脚':6,'バネ':7, 'ｸｯｼｮﾝ':8, 'HYPERFLEX':9,'ﾛｻﾞｰﾅ':10, '旧モデル':11,'キャンセル不可品':12}

from .models import TfcCode

def get_z():
    #在庫フラグのコードを取得
    result = [] #[コード, カテゴリー] の配列
    zcodes = TfcCode.objects.filter(zaiko = 1).values('hcode', 'cat')
    for zcode in  zcodes:
        result.append(list(zcode.values()))

    return result

def get_k():
    #検討フラグのコードを取得
    result = [] #[コード, カテゴリー] の配列
    kcodes = TfcCode.objects.filter(kento = 1).values('hcode', 'vol', 'cat')
    for kcode in  kcodes:
        result.append(list(kcode.values()))

    return result


def ori_sort(result):
    catn = lambda val:CAT_ORDER[val[-1]]
    model = lambda val:val[0].split('-')[0].replace('I', '')
    pie = lambda val:val[0].split('-')[-1] 
    fab = lambda val:val[0].split(' ')[-1]
    result = sorted(result, key=pie)
    result = sorted(result, key=fab)
    result = sorted(result, key=model)
    result = sorted(result, key=catn)
    return result

def print_menu(result):
    if len(result[0]) == 2:
        for row in result:
            print(row[0], row[1])

    elif len(result[0]) == 3:
        for row in result:
            print(row[0], row[1], row[2])

#print(get_z())
#print_menu(get_k())
#print_menu(ori_sort(get_z()))
