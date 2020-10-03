#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import datetime as dt

#納期は'yyyy/mm/dd'形式なので、/でスプリットして、int()で数のリストを作成
#datetime形式に変換
#スラッシュバージョン
def s2d(hiduke):
    hlist = hiduke.split('/')
    hlist = [int(x) for x in hlist]

    return dt.date(*hlist)

#ハイフォンバージョン
def s2dh(hiduke):
    hlist = hiduke.split('-')
    hlist = [int(x) for x in hlist]

    return dt.date(*hlist)

#逆バージョン 日付データから文字列
def d2s(hiduke):
    return hiduke.strftime('%Y/%m/%d')

#逆ハイフォンバージョン 日付データから文字列
def d2sh(hiduke):
    return hiduke.strftime('%Y-%m-%d')



