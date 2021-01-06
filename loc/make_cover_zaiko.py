#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import csv

def juchu_su(models, koshinbi):
    juchu_q = {}  #受注数量

    #models辞書のキー(モデル名)をリストで
    model_names = sorted(models)

    for name in model_names:
        total = 0
        for line in models[name]:
            if line[1] > koshinbi :
                total += int(line[2])

        juchu_q[name] = total

    #print('juchu', juchu_q)
    return juchu_q

    
#モデル別在庫数辞書作成

def zaiko_su(bdata):
    zaiko_q = {}  #在庫数量
    for row in bdata:
        if row[1] in zaiko_q:
            zaiko_q[row[1]] += row[2]
        else:
            zaiko_q[row[1]] = row[2]

    del zaiko_q['empty']

    #print('zaiko', zaiko_q)
    return zaiko_q

#print(zaiko_q)

#カバー在庫・受注数リストの作成
def write_cover_zaiko(zaiko_q, juchu_q):
    cover_z =[]

    for k, v in zaiko_q.items():
        cover_z.append([k, v, 0])

    for k, v in juchu_q.items():
        flag = 0
        for row in cover_z:
            if k == row[0]:
                row[2] = v
                flag = 1

        if flag == 0:
            cover_z.append([ k, 0, v ])

    cover_z.sort()

#    with open('cover_zaiko.csv', 'w', encoding='CP932') as f:
#        writer = csv.writer(f)
#        writer.writerows(cover_z)

    print('cover_zaiko.csv を書きだしました。')
    return cover_z


def make_cover_zaiko(models, koshinbi, bdata):
    return write_cover_zaiko(zaiko_su(bdata), juchu_su(models, koshinbi))



