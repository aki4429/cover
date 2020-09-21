#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import datetime as dt

#納期は'yyyy/mm/dd'形式なので、/でスプリットして、int()で数のリストを作成
#datetime形式に変換
def s2d(hiduke):
    hlist = hiduke.split('/')
    hlist = [int(x) for x in hlist]

    return dt.date(*hlist)

