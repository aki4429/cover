
# Seisanモデルから、key=コード,item=[[om,date,qty]..]の辞書、
#Locdata から　[番地、コード、数量]のリスト
#を作り、make_cover_zaiko に渡して、
#コード|在庫|受注残 のリストを出す。

from .models import Locdata, Seisan, LocStatus
from .make_cover_zaiko import make_cover_zaiko


def make_models():
    seisans = Seisan.objects.all()
    models = {} #モデルをキーにした辞書
    #モデル別のom, 生産日, 数量のリストを複数格納する
    for s in seisans:
        if s.code in models:
            models[s.code].append([s.om, s.seisan, s.qty])
        else:
            models[s.code] = []
            models[s.code].append([s.om, s.seisan, s.qty])

    return models

#banch, code, qty

def make_locs():
    locs = Locdata.objects.all()
    banches = []
    for loc in locs:
        banches.append([loc.banch, loc.code, loc.qty])

    return banches

def pick_koshinbi():
    ls = LocStatus.objects.all()
    return ls.first().koshinbi


def make_zaiko():
    return make_cover_zaiko(make_models(), pick_koshinbi(), make_locs())

