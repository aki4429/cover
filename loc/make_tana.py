#番地順のTFC縫製カバー入荷データ(モデル)を受け取って
#inputs = LocData.objects.order_by('banch')
#棚卸用に箱に添付するラベルのデータを作成する

#HEADDER = ["code", "piece", "fab", "address"]

def tana(inputs, bangos):
    data = []
    #data.append(HEADDER)
    for row in inputs:
        #empty は除く
        if len(row.code.split("-")) >1 :
            line=[]
            #item =row.code.split("-")[0].replace("013", "")
            item =row.code.split("-")[0]
            piece =row.code.split("-")[1].split(" ")[0]
            fab =row.code.split("-")[1].split(" ")[1]
            line.append(item)
            line.append(piece)
            line.append(fab)
            line.append(row.banch)
            #背番号リストとコードが一致するとき
            for ban in bangos:
                if row.code == ban.hcode: 
                    line.append(ban.se)

            data.append(line)
                
    return data
