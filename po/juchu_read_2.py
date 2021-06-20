#!/usr/bin/env python
# -*- coding: utf-8 -*-

#受注実績表を読み込み、TFC発注品のみ取り出す
#受注データからhinbanコードに置き換え、TfcCodeにあるか確認
#あるか、ないかをflag に記入
#cu37セット品はsetカウント, LH03はLegを追加
#Cart モデルにインサート

#読み出し項目位置(0から数えて)
JUCHUN = 1 #受注伝票№
JUCHUD = 0 #受注日
NOKI = 29 #納期(出荷日)
QTY = 73 #受注数
SOKO= 34 #倉庫コード
OCODE = 64 #obic商品コード (追加)
HINMEI = 65 #品名 (追加)
KIKAKU = 66 #規格 (追加)

HIN=56 #品目CD
SHI=57 #仕様
PIE=58 #ピース
PAR=59 #パーツ
IRO=60 #色
NU1=61 #布地1
NU2=62 #布地2
TOK=63 #特


import csv
from .hinmoku_2 import Hinmoku #品目名クラス・品目コードを加工修正したりするため
from .data_kako import check_code, make_set, make_leg
from .models import TfcCode, Cart

class JuchuRead:
    def __init__(self, filename):
        self.data = []
        self.data = self.read(filename) #必要項目をdataに読み出し

    #加算リストをバラバラと作らないために合算する関数
    def plus_if_exist(self, data, cart):
        for row in data:
            #コードとom番号が同じの場合、数量を加算
            if row.hinban == cart.hinban and row.om == cart.om :
                row.qty += cart.qty
                return data
        #同じものがなければ、レコードを追加
        return data.append(cart)

    def read(self, filename):
        with open(filename, 'r', encoding='CP932') as csvfile:
            data = []
            reader = csv.reader(csvfile)
            next(reader)
            for row in reader: #品目名,受注伝票№,受注日,納期,受注数
                hinmoku_data=[]
                hinmoku_data.append(row[HIN])
                hinmoku_data.append(row[SHI])
                hinmoku_data.append(row[PIE].zfill(2))
                hinmoku_data.append(row[PAR])
                hinmoku_data.append(row[IRO])
                hinmoku_data.append(row[NU1])
                hinmoku_data.append(row[NU2])
                hinmoku_data.append(row[TOK])
                h = Hinmoku(hinmoku_data)
                #バイオーダーか確認 and 除外モデルか確認
                #倉庫コードがA10000か
                if (h.is_byorder() or h.is_fujiei() ) and row[SOKO] == 'A10000' and not h.jogai() :
                    #データ構造=コード, 受注No.,受注日,納期,数,Oコード,
                    #品名,規格,セットフラグはゼロ
                    cart = Cart(
                        hinban= h.make_code(),
                        om = row[JUCHUN],
                        juchubi = row[JUCHUD].replace('/', '-'),
                        noki = row[NOKI].replace('/', '-'),
                        qty = int(float(row[QTY])),
                        obic = row[OCODE], 
                        hinmei = row[HINMEI], 
                        kikaku = row[KIKAKU],
                        set = 0,
                        )
                    self.plus_if_exist(data, cart)

        return data

    def show(self, data):
        for cart in data:
            #print(cart.hinban, cart.om, cart.qty, cart.obic, cart.hinmei, cart.kikaku, cart.set)
            print(cart.hinban, cart.qty, cart.om, cart.set, cart.flag, cart.obic )

    #カートに入れるデータを作成
    def get_juchu(self):
        data = make_set(make_leg(self.data))
        data = check_code(data)
        data.sort()
        #self.show(data)
        return data

    def save_torikomi(self, data):
        # 書き出し用のファイルを開く
        #self.data = data_kako.kako_add(self.data)
        #self.data = data_kako.sum(self.data)
        #self.data = data_kako.check(self.data, self.codes)
        with open(TORIOUT, "a", encoding="CP932") as out_file:
            writer = csv.writer(out_file,lineterminator='\n')
            for row in data:
                writer.writerow(row)

#FILENAME = 'media/juchu/juchu_20210531.csv'
#FILENAME = '/media/akiyoshi/Transcend/obic_new/juchu_data/juchu_20210222.csv'

#k = JuchuRead(FILENAME)
#data = make_set(k.data)
#data = make_leg(k.data)

