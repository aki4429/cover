#エクセルのインボイスから、hcode名と数量を取り出す。
#同じhcode名があったら加算する。
#hcode は,'013CH2'から始まるもので、zaikoフラグが1だけ
#抽出


import xlrd

from po.models import TfcCode

SHEET_NAME = 'INVOCE' #sheet名がINVOCEだけ対象
BEGIN_ROW = 12 #０から数えてデータが始まる行

#品名、数量はゼロから数えて左から何列目？
PO_COL = 0
ITEM_COL = 2 #品名列
QTY_COL = 3 #数量列

INVN = (2,0) #inv.#位置

def pick_items(filename):
    book = xlrd.open_workbook(filename)
    sheet = book.sheet_by_name(SHEET_NAME)

    #インボイスナンバー取得
    invn = sheet.cell(*INVN).value.replace("Invoice No:","")

    itemdic = {}

    #データ始まり行から最終行まで
    for row_index in range(BEGIN_ROW, sheet.nrows):
        item_name = sheet.cell(row_index, ITEM_COL).value
        qty = sheet.cell(row_index, QTY_COL).value
        #アイテム名が同じかつ在庫フラグが1
        code = TfcCode.objects.filter(item = item_name, zaiko = 1)

        #Item 列のセルが空白になったら、終わり
        if len(item_name) == 0 :
            break
        elif len(code) == 1: 
            h_code = code[0].hcode
            if h_code.startswith('013CH2'):
                if h_code not in itemdic:
                    itemdic[h_code] = qty
                else:
                    itemdic[h_code] += qty

    return itemdic, invn


#items = pick_items('/home/akiyoshi/Downloads/TI201222A FUGUE.xls')
#print(items)


