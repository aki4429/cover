#!/usr/bin/env python
# -*- coding: utf-8 -*-

#ピック指示モデルPick の 生産日配列 
#から、フォームのプルダウンリスト用の
#Choice リストを作成する。
# Pick.objects.all().values('seisan')[0] 
# = {'seisan':datetime.date(xx, x, x,)}

from .s2d import d2sh
from .models import Pick

def p2d():
    picks =  Pick.objects.all().values('seisan') 
    days = []
    for pick in picks:
        days.append(d2sh(pick['seisan']))

    dayslist =  list(set(days))
    dayslist.sort()
    choice_list = []
    for dl in dayslist:
        choice_list.append((dl, dl))

    return tuple(choice_list)


