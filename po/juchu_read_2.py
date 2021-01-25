#!/usr/bin/env python
# -*- coding: utf-8 -*-

#受注実績表を読み込み、TFC発注品のみ取り出す

#受注実績データファイル名
FILEOUT = "kako_juchu.csv"
TORIOUT = "torikomi_juchu.csv"

#読み出し項目位置(0から数えて)
#A_1 = 6 #品目CD
#A_2 = 66 #品目名
A_3 = 1 #受注伝票№
A_4 = 0 #受注日
A_5 = 29 #納期(出荷日)
A_6 = 73 #受注数
A_7 = 34 #倉庫コード
A_8 = 64 #商品コード (追加)

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
from .data_kako import kako_add, sum, check
from .models import TfcCode

class JuchuRead:
    def __init__(self, filename):
        self.data = []
        self.codes = []
        self.read(filename) #必要項目をdataに読み出し
        self.codes = self.read_sql() #CODE マスターを読み込み
        #self.save_torikomi(self.data)
        #self.save_juchu(self.data)

    def read(self, filename):
        with open(filename, 'r', encoding='CP932') as csvfile:
            reader = csv.reader(csvfile)
            next(reader)
            for row in reader: #品目名,受注伝票№,受注日,納期,受注数
                #print("row={0}:".format(A_2) + row[A_2])
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
                #h.print_detail()
                #バイオーダーか確認 and 除外モデルか確認
                #倉庫コードがA10000か
                if (h.is_byorder() or h.is_fujiei() ) and row[A_7] == 'A10000' and not h.jogai() :
                    self.data.append([h.make_code(),row[A_3],
                        row[A_4],row[A_5],int(float(row[A_6])),row[A_8]]) #A_8を末尾に追加
                        #row[A_4],row[A_5],int(float(row[A_6]))])

    def read_sql(self):
        tfcs = TfcCode.objects.all()
        data = []
        for cd in tfcs:
            data.append([cd.id, cd.hinban])

        return data

    def show(self):
        for c in self.data:
            print(c)

    def show_ng(self):
        print("=" * 70)
        for c in self.data:
            if c[5] =="NO" or c[5] == "Double" :
                print(c)

    def get_juchu(self):
        # カートに入れるデータを作成
        data = kako_add(self.data)
        data = sum(data)
        data = check(data, self.codes)
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


#k = JuchuRead(FILENAME)
#print(k.get_date())
#k.show()
#k.show_ng()
