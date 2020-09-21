#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#shijiname = glob.glob('./shiji/*.csv')[-1]

import glob
import csv

from .s2d import s2d

#縫製品カバーコードに変換
def repl(code):
    model = code[:8].strip()
    piece = code[11:17].strip()
    fab1 = code[24:31].strip()
    #CH232で35,37で無い場合
    if 'CH232' in model and piece != '35' and piece != '37' :
        model = "013" + model + 'WI'
    elif 'CH232' in model and (piece == '35' or piece == '37') :
        model = "013" + model + 'W'
    elif 'CH271' in model and (piece != '35' and piece != '37') :
        model = "013" + model + 'I'
    elif 'CH232-35' in model :
        model = model.replace('CH232-35', 'CH232W-35')
    elif 'CH232-37' in model :
        model = model.replace('CH232-37', 'CH232W-37')
    else:
        model = "013" + model 

    return model + "-" + piece + "C " + fab1


def read_shiji(shijiname):
    #shijiname = glob.glob('../media/shiji/*.csv')[-1]
    #shijiname = glob.glob('media/shiji/*.csv')[-1]
    sdata=[]
    #shiyo 製品コード1 製番4 納期5 指示数6 
    #shiji 規格23 製番55 製造開始日27 製品数 35 担当者13　=8205:検査 63 製造ステータス !=中止
    #CH232とCH271の仕様[8:11]=国産(N/NN)または、パーツ[17:19]=本体のみ(B/GB)
    #以外で、バイオーダー(Z)でないもの
    with open( shijiname, encoding='CP932') as f:
        reader = csv.reader(f)
        for row in reader:
            if (row[13]=="8205" and row[23][8:11].strip() != "N" and row[23][8:11].strip() != "NN" and row[23][8:11].strip() != "NE" and row[23][17:19].strip() !="B" and row[23][17:19].strip() != 'GB' ) and  ('CH232' in row[23][:8].strip() or 'CH271' in row[23][:8]) and  row[23][39:40].strip() != "Z" and row[84].strip() != "中止" : 
                sdata.append([repl(row[23]), row[55], s2d(row[27]), row[35]])
    
    print('製造指示書：', shijiname, 'を読み込みました。')
    
    return sdata

