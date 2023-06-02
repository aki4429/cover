#!/usr/bin/env python
# -*- coding: utf-8 -*-

#オービックの発注検討表から在庫報告、発注検討表作成用に
#在庫と受注数をとりだす。

import csv
import os
import glob

from .hin_slice import bunkai
from .hinmoku_2 import Hinmoku

#ロケーション管理の在庫受注データ取り出し
from loc.cover_zaiko import make_zaiko

from .models import Fabric

NNAME = './zaiko_d/nunoji_hinban.csv'
#CNAME = './zaiko_d/cover_zaiko.csv'

def read_nunohin():
    #オリジナル布地名と新コードのデータを読み込む
    fabs = Fabric.objects.all()
    data = []
    for fab in fabs:
        data.append([fab.name, fab.code])

    return data

#カバー在庫取込み
def read_cov():
    d = make_zaiko()
    return  d


def rep_nuno(code):
    #布オリジナル番号は読み替える
    nuno_data = read_nunohin()
    for nuno in nuno_data:
        if nuno[0] in code:
            code = code.replace(nuno[0], nuno[1])

    return code

def sum_list(data):
    #コードが同じデータの在庫数と受注数を加算して一つにまとめる。
    code ={}  #キーをコード、値を在庫と受注のリスト[在庫,受注]の辞書
    c_data = [] #まとめたデータ保管用変数

    for row in data:
        code.setdefault(row[0], [0,0])
        code[row[0]] = [ x + y for (x,y) in zip(code[row[0]], [row[1], row[2]])]

    #辞書からリストに戻す
    for k, v in code.items():
        c_data.append([k] + v)

    return c_data

#obic発注検討表 csv のfilename と ロケーション管理の
#カバー在庫(cover_zaiko.csv)を受け取って品名,在庫,受注数の一覧と
#基準日を返す
def read_kh_2(k_filename):
    covd =  read_cov() #カバーデータを読み込む
    data = []
    #発注検討表を読み込む
    with open(k_filename, 'r', encoding='CP932') as csvfile:
        reader = csv.reader(csvfile)
        next(reader)
        for row in reader: 
            #商品コード10, 規格12,現在在庫南濃倉庫-開始日以前出庫予定数,
            # 受注数-出庫予定数
            kijunbi = row[6] #基準日6を取り込み
            if row[10].startswith('0'):
                #商品コードが０で始まるものは材料なのでキーは商品コード
                if not row[10].startswith('0132'):
                    #ただし、0132で始まるカバーはロケーション管理のため除外
                    if row[10].startswith('013'):
                        #コード文字数制限で省略したCHを戻しておく
                        row[10] = row[10].replace('013', '013CH')

                data.append([row[10], int(float(row[17]))-int(float(row[20])),
                    int(float(row[126]))-int(float(row[20]))])
            elif not row[10].startswith('1'):
                #1で始まる余計な材料コードは除く
                row[12] = rep_nuno(row[12]) #布地コード読替え
                h = Hinmoku(bunkai(row[12]))
                if h.is_kansei() or not h.is_byorder():
                #if h.is_kansei() :
                    data.append([h.make_code(), int(float(row[17]))-int(float(row[20])),
                    int(float(row[126]))-int(float(row[20]))])

    data = data + covd
    data = sum_list(data)
    data.sort()
    return data, kijunbi

#for row in data:
#    print(row[0], row[1], row[2])

#print(read_kh()[1])
#print(row[0], row[1])
#print('data', data)


import pandas as pd

def read_kh(k_filename):
    #covd =  read_cov() #カバーデータを読み込む
    USECOL = ["商品コード", "規格", "現在在庫南濃倉庫", "開始日以前出庫予定数", "受注数", "出力開始日"]
    data = []
    #発注検討表からUSECOL項目だけ抽出して読み込む
    df = pd.read_csv(k_filename, encoding='CP932', usecols=USECOL)
    #USECOLの順番通りに列を並べ替える
    df = df.reindex(columns=USECOL)
    #検討表の取り出した内容をリストに変換
    kentos = df.values.tolist()

    for row in kentos: 
        #商品コード0, 規格1,現在在庫南濃倉庫2-開始日以前出庫予定数3, # 受注数4-開始日以前出庫予定数3
        kijunbi = row[5] #基準日5を取り込み
        if row[0].startswith('0'):
            #商品コードが０で始まるものは材料なのでキーは商品コード
            #if not row[10].startswith('0132'):
                #ただし、0132で始まるカバーはロケーション管理のため除外
            if row[0].startswith('013'):
                #コード文字数制限で省略したCHを戻しておく
                row[0] = row[0].replace('013', '013CH')

            data.append([row[0], int(float(row[2]))-int(float(row[3])),
                int(float(row[4]))-int(float(row[3]))])
        elif not row[0].startswith('1'):
            #1で始まる余計な材料コードは除く
            row[1] = rep_nuno(row[1]) #布地コード読替え
            h = Hinmoku(bunkai(row[1]))
            if h.is_kansei() or not h.is_byorder():
            #if h.is_kansei() :
                data.append([h.make_code(), int(float(row[2]))-int(float(row[3])),
                int(float(row[4]))-int(float(row[3]))])

    #data = data + covd
    data = sum_list(data)
    data.sort()
    #with open("kento_list.csv", 'w', encoding='CP932') as f:
    #    writer = csv.writer(f)
    #    writer.writerows(data)
    return data, kijunbi


