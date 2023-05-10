#!/usr/bin/env python
# -*- coding: utf-8 -*-

#インボイスを読み込んで、品名、数量のデータを取り出す
#データDBに登録し、登録結果を保存する
#インボイス行から、pon, item を読み取り、該当するpoline を取得
#poline が複数該当すれば、invline の数量のあるだけ、invlineを
#複数行に増やして登録
#polineのbalanceを減らしてupdate

from .models import Inv, Invline, TfcCode, Po, Poline
import os
import xlrd
import datetime
from dateutil.parser import parse


#０から数えてデータが始まる行
#BEGIN_ROW = 12
BEGIN_ROW = 10
#CONTAINER_ROW = 2
CONTAINER_ROW = 3

#品名、数量はゼロから数えて左から何列目？
PO_COL = 0
ITEM_COL = 2
QTY_COL = 3
#UP_COL = 5

#INVN = (3,0) #inv.#位置
INVN = (3,3) #inv.#位置
#ETD = (9,0) #ETD位置
ETD = (8,3) #ETD位置

#SHEET_NAME = "INVOCE"
SHEET_NAME = "INV"
SFILE = "tfc_cover.sqlite"

class ReadInv:
    def __init__(self, fname):

        book = xlrd.open_workbook(fname)
        sheet = book.sheet_by_name(SHEET_NAME)

        self.invn = self.get_invn(sheet)
        self.etd = self.get_etd(sheet)

        #sheet名にContainerがあれば、その数を返す
        containers = self.ifcontainers(book)

        if containers == 0 :
            inv = self.insert_inv(self.invn, self.etd)

            #def insert_invline(self, sheet, inv, begin_row):
            self.insert_invline(sheet, inv, BEGIN_ROW)
            #con.commit()
        else:
            for i in range(1, containers + 1):
                sheet = book.sheet_by_name('Container' + str(i))
                inv = self.insert_inv(self.invn+str(i), self.etd)
                self.insert_invline(sheet, inv, CONTAINER_ROW)

    def get_invn(self, sheet):
        return sheet.cell(*INVN).value.replace("Invoice No:","")
        
    def get_etd(self, sheet):
        etd = parse(sheet.cell(*ETD).value.replace("ETD:","" ).replace("、", ",").replace(".0", ". 0").replace(".1", ". 1").replace(".2", ". 2").replace(".3", ". 3").replace("，", ","))
        return etd.strftime("%Y-%m-%d")

    def ifcontainers(self, book):
        sheets = book.sheet_names()
        counter = 0
        for sn in sheets:
            if 'Container' in sn:
                counter += 1

        return counter

    #インボイスデータ(Inv.NO. ETD)をDBに登録、idを返す。
    def insert_inv(self, invn, etd):
        i = Inv(invn = invn, etd = etd)
        i.save()
        print("invn", invn)
        return i

    def insert_invline(self, sheet, inv, begin_row):
        #データ始まり行から最終行まで
        keep_pon=""
        for row_index in range(begin_row, sheet.nrows):
            pon = sheet.cell(row_index, PO_COL).value
            #PO NO. ブランク行は、上のセルのPO NO.
            if len(pon) != 0:
                keep_pon = pon
                #poのbalanceを初期化しておく。
                po = Po.objects.filter(pon=pon).first()
                data=[]
                pls = Poline.objects.filter(po=po)
                pl_update =[] #bulk 一括update用にクラスを格納
                for pl in pls:
                    ils = Invline.objects.filter(poline = pl)
                    #引当インボイスの数量の合計
                    sum = 0
                    for il in ils:
                        sum += il.qty
                    #残数を計算して更新
                    pl.balance = pl.qty - sum
                    pl_update.append(pl)
                Poline.objects.bulk_update(pl_update, fields=['balance'])

            else:
                pon = keep_pon

            item = sheet.cell(row_index, ITEM_COL).value
            qty = sheet.cell(row_index, QTY_COL).value
            #Item 列のセルが空白になったら、終わり
            if len(item) == 0 :
                break
            else:
                #code_オブジェクト取得
                result = TfcCode.objects.filter(item=item)
                #見つからなかったら、resultの長さはゼロ
                #見つからない場合は対象外
                if len(result) != 0:
                    code = result.first()
                    #インボイス行の残数量がゼロになるまで繰り返す
                    while(qty > 0):
                        #poline オブジェクト 取得
                        #Polineでponとitemが同じでPO残がゼロより大きい
                        #cur.execute("select p.id from poline p inner join tfc_code\
                        #        c on p.code_id = c.id, po o on p.po_id = o.id\
                        #        where o.pon = ? and c.item = ? ", (pon, item))
                        pls=Poline.objects.filter(po__pon=pon, code__item=item, balance__gt=0)
                        #複数あった場合は、最初のものを対象に
                        if len(pls) >0 :
                            poline = pls.first()
                            #po残量balanceが invlineのqty以上のとき
                            if poline.balance >= qty :
                                #インボイス行の登録
                                il = Invline(code=code, qty=qty, inv = inv, poline = poline, item = item)
                                il.save()
                                #cur.execute("INSERT INTO invline ( code_id , qty,\
                                #inv_id, poline_id , item ) VALUES( ?, ?, ?, ?, ?)",
                                #(codeid, qty, invid, polineid, item))
                                #PO行の残を減らします。
                                poline.balance = poline.balance - qty
                                poline.save()
                                qty = 0
                                #cur.execute("UPDATE poline SET balance = (balance - ?) where id = ? ", (qty, polineid))
                            #po残量balanceが invlineのqtyより小さいとき
                            else:
                                il = Invline(code=code, qty=poline.balance, inv = inv, poline = poline, item = item)
                                il.save()
                                #インボイス行の数量を減らします。
                                qty = qty - poline.balance
                                #PO行の残はゼロになります。
                                poline.balance = 0
                                poline.save()

                        #polineの該当ない場合は登録してループから抜ける。
                        elif len(pls) <= 0:
                            il = Invline(code=code, qty=qty, inv = inv, item = item)
                            il.save()
                            qty=0

                #コードがない場合も登録
                else:
                    il = Invline(qty=qty, inv = inv, item = item)
                    il.save()

                    





#r = ReadInv()
