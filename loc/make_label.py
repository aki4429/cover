#番地順のTFC縫製カバー入荷データ(モデル)を受け取って
#inputs = Input.objects.order_by('banch')
#整理用の箱に添付するラベル用のデータを作成する

#HEADDER = ["code", "piece", "fab", "address"]

def kako(inputs):
    data = []
    #data.append(HEADDER)
    for row in inputs:
        if int(float(row.kqty)) == 0: #既存数量がゼロのとき
            line=[]
            item =row.hcode.split("-")[0].replace("013", "")
            piece =row.hcode.split("-")[1].split(" ")[0]
            fab =row.hcode.split("-")[1].split(" ")[1]
            line.append(item)
            line.append(piece)
            line.append(fab)
            line.append(row.banch)
            data.append(line)
                
    return data
