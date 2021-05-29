#!/usr/bin/env python
# -*- coding: utf-8 -*-

#新オービックの在庫表から、発注検討表作成用に
#消費実績をとりだす。

import csv
import os
import glob
from django.conf import settings
from po.models import Fabric

from .hin_slice import bunkai
from .hinmoku_2 import Hinmoku

from .index_tool import get_xindex, get_yindex

JDIR = 'jisseki_new'
NNAME = './zaiko_d/nunoji_hinban.csv'

def read_nunohin():
    #オリジナル布地名と新コードのデータを読み込む
    fabs = Fabric.objects.all()
    data = []
    for fab in fabs:
        data.append([fab.name, fab.code])

    return data


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


def read_shouhi():
    dir_name = os.path.join(settings.MEDIA_ROOT, JDIR, "*.csv")
    filenames = glob.glob(dir_name)
    data=[]
    for filename in filenames:
        #a= filename.split('-')
        #month = a[0][-2:]+a[1][:2]
        with open(filename, 'r', encoding='CP932') as csvfile:
            reader = csv.reader(csvfile)
            next(reader)
            for row in reader: 
                #会計年月8, 商品コード17, 規格19, 売上数43, 出庫数46,
                month = row[8][2:]
                if row[17].startswith('0') and int(float(row[46])) != 0 :
                    #商品コードが０で始まるものは材料なので商品コード+出庫数
                    old_code = row[17].replace('013', '013CH')
                    old_code = old_code.replace('013CH232W', '013CH232WI')
                    old_code = old_code.replace('013CH232WI-35', '013CH232W-35')
                    old_code = old_code.replace('013CH232WI-37', '013CH232W-37')
                    old_code = old_code.replace('013CH271-', '013CH271I-')
                    old_code = old_code.replace('013CH271I-35', '013CH271-35')
                    old_code = old_code.replace('013CH271I-37', '013CH271-37')
                    old_code = old_code.replace('014CH271N', '014CH271E')
                    data.append([month, old_code, int(float(row[46]))])
                elif int(float(row[43])) != 0: 
                    #商品は規格+売上数
                    row[19] = rep_nuno(row[19]) #布地コード読替え
                    h = Hinmoku(bunkai(row[19]))
                    if not h.is_byorder():
                        data.append([month, h.make_code(), int(float(row[43]))])

    data.sort()
    #with open('shouhi_data.csv', 'w') as f:
    #    writer = csv.writer(f)
    #    writer.writerows(data)
    return data

#data = read_nunohin(NNAME)

#data = read_shouhi()
#print(data)

def make_monthlist():
    dir_name = os.path.join(settings.MEDIA_ROOT, JDIR)
    files = os.listdir(dir_name)
    monthlist = []
    for f in files:
        monthlist.append( f.split('-')[0][-2:]+f.split('-')[1][:2])

    monthlist.sort()

    return monthlist

#print(make_monthlist())

def make_shouhi(codelist):
    monthlist = make_monthlist()
    data = read_shouhi()

    #消費表用の2次元配列を初期化してデータを代入する
    shouhi_hyo = [['' for i in range(len(monthlist)+1)] for j in range(len(codelist)+1)]

    #codelist.insert(0, "") #先頭行はタイトル行なので空けておく
    #1列目にコードを代入
    for i, code in enumerate(codelist):
        shouhi_hyo[i+1][0] = code

    #１行目にmonthを代入
    for i, m in enumerate(monthlist):
        shouhi_hyo[0][i+1] = m

    for row in data: #month, コード、当月出庫
        if get_yindex(shouhi_hyo, row[1]) is not None \
                and get_xindex(shouhi_hyo, row[0]) is not None :
            shouhi_hyo[get_yindex(shouhi_hyo, row[1])][get_xindex(shouhi_hyo, row[0])] = row[2]

    #with open('shouhi_hyo_new.csv', 'w', encoding='CP932') as f:
    #    writer = csv.writer(f)
    #    writer.writerows(shouhi_hyo)
    #    print('shouhi_hyo_new.csv を書きました。')

    return shouhi_hyo

#for row in data:
#    print(row[0], row[1], row[2])

#print(read_kh()[1])
#print(row[0], row[1])

