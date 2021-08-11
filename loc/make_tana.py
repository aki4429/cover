#番地順のTFC縫製カバー入荷データ(モデル)を受け取って
#inputs = LocData.objects.order_by('banch')
#棚卸用に箱に添付するラベルのデータを作成する

HEADDER = ["address", "code", "sebango", "qty"]

def tana(inputs, bangos):
    data = []
    data.append(HEADDER)
    for row in inputs:
        #empty は除く
        #if len(row.code.split("-")) >1 :
        line=[]
        #item =row.code.split("-")[0].replace("013", "")
        if row.code == 'empty':
            orig_code = 'empty'
        else:
            orig_code = row.code.replace('013CH', '013').replace('013271I', '013271').replace('013232WI', '013232W')
        #item =row.code.split("-")[0]
        #piece =row.code.split("-")[1].split(" ")[0]
        #fab =row.code.split("-")[1].split(" ")[1]
        line.append(row.banch)
        line.append(orig_code)
        #line.append(item)
        #line.append(piece)
        #line.append(fab)
        #背番号リストとコードが一致するとき
        for ban in bangos:
            if orig_code == 'empty':
                line.append(" ")
            elif orig_code == ban.hcode: 
                line.append(ban.se)

        line.append(row.qty)
        data.append(line)
                
    return data


