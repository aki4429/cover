
#生産数量分のピック指示を作ります。

def pickup(seis, locs): #生産リストとロケーションリストを受け取ります。
    picks = []
    for sei in seis:
        for loc in locs:
            if sei['qty'] != 0 and loc['qty'] != 0 and sei['code'] == loc['code']:
                if sei['qty'] <= loc['qty']:
                    picks.append([sei['code'], sei['qty'], loc['qty'],
                        sei['seisan'], sei['om'], loc['banch']])
                    loc['qty'] = loc['qty'] - sei['qty']
                    sei['qty'] = 0

                else:  #生産数が箱数より多い時
                    picks.append([sei['code'], loc['qty'], loc['qty'],
                        sei['seisan'], sei['om'], loc['banch']])
                    sei['qty'] = sei['qty'] - loc['qty']
                    loc['qty'] = 0

        if sei['qty'] != 0:
            picks.append([sei['code'], sei['qty'], 0,
                sei['seisan'], sei['om'], 'mitei'])
    
    return picks



