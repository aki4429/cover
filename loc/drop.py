#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#Locdataのリストで落ちるケースの番地変換
#locs = Locdata.objects.all()

def drop(locs):
    uppers = [] #1段目、3段目で数量0でないリスト
    for loc in locs:
        dan = loc.banch.split('-')[2] 
        if (dan == '1' or dan == '3') and loc.qty != 0 :
            uppers.append(loc)

    for ue in uppers:
        #2段目、3段目が0のケースを探します。
        shita = ue.banch.replace('1', '2').replace('3', '4')
        for loc in locs:
            if loc.banch == shita and loc.qty == 0:
                #上下の番地を置き換えます。
                loc.banch = ue.banch
                ue.banch = shita

    return locs


