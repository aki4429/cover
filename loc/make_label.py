#番地順のTFC縫製カバー入荷データ(モデル)を受け取って
#inputs = Input.objects.order_by('banch')
#整理用の箱に添付するラベル用のデータを作成する

#HEADDER = ["code", "piece", "fab", "address"]

def kako(inputs, bangos):
    data = []
    #data.append(HEADDER)
    for row in inputs:
        #既存数量がゼロのとき
        if int(float(row.kqty)) == 0 :
            line=[]
            #item =row.hcode.split("-")[0].replace("013", "")
            item =row.hcode.split("-")[0]
            piece =row.hcode.split("-")[1].split(" ")[0]
            fab =row.hcode.split("-")[1].split(" ")[1]
            line.append(item)
            line.append(piece)
            line.append(fab)
            line.append(row.banch)
            #背番号リストとコードが一致するとき
            for ban in bangos:
                if row.hcode.replace('013CH', '013').replace('013271I', '013271').replace('013232WI', '013232W') == ban.hcode: 
                    line.append(ban.se)

            data.append(line)
                
    return data
