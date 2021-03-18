#番地順のTFC縫製カバー入荷データ(モデル)を受け取って
#inputs = Input.objects.order_by('banch')
#整理用の箱に添付するラベル用のデータを作成する

#HEADDER = ["code", "piece", "fab", "address"]

def kako(inputs, bangos):
    data = []
    #data.append(HEADDER)
    for row in inputs:
        for ban in bangos:
            #既存数量がゼロのときで背番号リストとコードが一致する
            if int(float(row.kqty)) == 0 and row.hcode == ban.hcode: 
                line=[]
                item =row.hcode.split("-")[0].replace("013", "")
                piece =row.hcode.split("-")[1].split(" ")[0]
                fab =row.hcode.split("-")[1].split(" ")[1]
                line.append(item)
                line.append(piece)
                line.append(fab)
                line.append(row.banch)
                line.append(ban.se)
                data.append(line)
                
    return data
