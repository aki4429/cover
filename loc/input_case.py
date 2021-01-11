#入荷カバーのコード/数量リストから、箱入れ用のリストを作る。
#既存箱のリストと、空箱リストの収容最大値まで、入荷したカバーを
#割り振って、片付けられるようにする。

#from loc.models import Locdata, Addcover

#ピース毎の最大収容数
MAX_DIC={'03':4, '06':4, '07':4, '08':4, '09':4, '17':8, '20':4, '20N':4, '35':30, '37':20, '41':4, '42':4, '49':4, '50':4}

#コードのピース番号を取り出し、max 数を確定
def get_max(code):
    piece = code.split("-")[1].split('C')[0]
    return MAX_DIC[piece]


def make_input(Locdata, Addcover, Input):
#def make_input_list():
    #前の内容は全削除する。
    Input.objects.all().delete()
    inputs = [] #Inputモデルをリストで格納。後で bulk_create
    #Inputモデル[番地、コード、数量、既存数]
    #Input:banch, hcode, qty, kqty

    adds = [] #到着カバーのリスト用
    locs = [] #番地カバーのリスト用

    for ac in Addcover.objects.all():
        adds.append([ac.hcode, int(float(ac.qty))])

    for loc in Locdata.objects.all():
        locs.append([loc.banch, loc.code, int(float(loc.qty))])

    #空箱番地表を作る
    empties = []
    for loc in locs:
        if loc[1] == 'empty':
            empties.append(loc[0])

    #到着カバーを一つづつ見ていく
    for ac in adds:
        balance = int(float(ac[1]))
        max = get_max(ac[0]) #収納最大数
        kizons = [] #コードが同じ在庫ケースの情報をとる[番地、収納可能数]
        for loc in locs:
            if ac[0] == loc[1] and (max- loc[2]) > 0: #可能数がない箱は除く
                kizons.append([loc[0], max - loc[2]])

        #在庫ケースがあれば、可能数を当て込んでいく
        if len(kizons) > 0 :
            for kizon in kizons :
                if balance > kizon[1] : #残りが収納可能数より多い
                    #[番地, コード, 数量(最大可能数), 既存数]
                    input = Input(banch=kizon[0], hcode=ac[0], 
                            qty=kizon[1], kqty=(max - kizon[1]) )
                    inputs.append( input)
                    #inputs.append([kizon[0], ac[0], kizon[1], max - kizon[1] ])
                    balance -= kizon[1]
                elif balance > 0:
                    #[番地, コード, 数量(残り全部), 既存数]
                    input = Input(banch=kizon[0], hcode=ac[0],
                            qty = balance, kqty= (max - kizon[1]) )
                    inputs.append( input)
                    #inputs.append([kizon[0], ac[0], balance, max - kizon[1] ])
                    balance = 0 #全部入れちゃったので残りはゼロ

        #残りがあれば、
        if balance > 0 :
            while balance > 0 :
                if balance > max :
                    #[番地, コード, 数量(最大可能数), 既存数]emptyは減っていく
                    input = Input(banch=empties.pop(0), hcode=ac[0],
                            qty = max, kqty = 0 )
                    inputs.append( input)
                    #inputs.append([empties.pop(0), ac[0], max, 0 ])
                    balance -= max
                else:
                    #[番地, コード, 数量(残り全部), 既存数]emptyは減っていく
                    input = Input(banch=empties.pop(0), hcode=ac[0], 
                            qty = balance, kqty = 0 )
                    inputs.append( input)
                    #inputs.append([empties.pop(0), ac[0], balance, 0 ])
                    balance = 0 #全部入れちゃったので残りはゼロ

    #Input.objects.bulk_create(inputs) 
    #input_cases = Input.objects.order_by('hcode')
    Input.objects.bulk_create(inputs) 
    inputs = Input.objects.order_by('hcode')
    return inputs
