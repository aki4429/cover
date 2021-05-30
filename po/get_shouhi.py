#!/usr/bin/env python
# -*- coding: utf-8 -*-

#オービックの旧在庫表から、発注検討表作成用に
#消費実績をとりだす。

import csv
import os
from po.models import Fabric, Shouhi

from .hin_slice import bunkai
from .hinmoku_2 import Hinmoku

from .get_shouhi_new import read_nunohin, rep_nuno, sum_list

def read_shouhi_old(filepath):
    data = []
    a= filepath.split('-')
    month = a[0][-2:]+a[1][:2]
    with open(filepath, 'r', encoding='CP932') as csvfile:
        reader = csv.reader(csvfile)
        next(reader)
        for row in reader: 
            #品目コード6, 品目名7, 当月出庫18, 在庫場所 9, 在庫状態 11
            if row[9] == "南濃倉庫" and row[11] == "通常":
                #商品コードが０で始まるものは材料なのでキーは品目コード
                if row[6].startswith('0') and int(float(row[18])) != 0 :
                    data.append([row[6], int(float(row[18]))])

                elif int(float(row[18])) != 0 : 
                    #商品はキーは品目名
                    row[7] = rep_nuno(row[7]) #布地コード読替え
                    h = Hinmoku(bunkai(row[7]))
                    if not h.is_byorder():
                        data.append([ h.make_code(), int(float(row[18]))])

    sum_data = sum_list(data)
    shouhis = []
    for row in sum_data:
    	shouhis.append(Shouhi(month=month, code = row[0], qty = row[1]))
    
    Shouhi.objects.bulk_create(shouhis)


