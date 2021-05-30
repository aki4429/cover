#!/usr/bin/env python
# -*- coding: utf-8 -*-

#新オービックの在庫表から、発注検討表作成用に
#消費実績をとりだす。

import csv
import os
from po.models import Fabric, Shouhi

from .hin_slice import bunkai
from .hinmoku_2 import Hinmoku

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

#コードが同じものがあれば、一つにまとめる
def sum_list(data):
    sum_data={}
    for row  in data:
        if row[0] in sum_data:
            sum_data[row[0]] += row[1]
        else:
            sum_data[row[0]] = row[1]

    return list(sum_data.items())

def read_shouhi(filepath):
    data = []
    print('filepath:', filepath)
    with open(filepath, 'r', encoding='CP932') as csvfile:
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
                data.append([old_code, int(float(row[46]))])
            elif int(float(row[43])) != 0: 
                #商品は規格+売上数
                row[19] = rep_nuno(row[19]) #布地コード読替え
                h = Hinmoku(bunkai(row[19]))
                if not h.is_byorder():
                    data.append([h.make_code(), int(float(row[43]))])

    sum_data = sum_list(data)
    shouhis = []
    for row in sum_data:
        shouhis.append(Shouhi(month=month, code = row[0], qty = row[1]))

    Shouhi.objects.bulk_create(shouhis)

