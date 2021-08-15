from django.db import models
from django.conf import settings
from po.models import TfcCode

class Locdata(models.Model):
    banch = models.CharField(max_length=50, blank=True, null=True)
    code = models.TextField(blank=True, null=True)
    qty = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'locdata'

    def __str__(self):
        return self.banch

class Shiji(models.Model):
    shiji_date = models.CharField(max_length=50, blank = True)
    file_name = models.FileField(upload_to='shiji/', verbose_name="ファイルを送信")
    uploaded_at = models.DateTimeField(auto_now_add=True)

class Seisan(models.Model):
    code = models.TextField(blank=True, null=True)
    om = models.CharField(max_length=50, blank = True)
    seisan = models.DateField(blank=True, null=True)
    qty = models.IntegerField(blank=True, null=True)

    def __str__(self):
        return self.om

class Pick(models.Model):
    code = models.TextField(blank=True, null=True)
    qty = models.IntegerField(blank=True, null=True)
    loc_qty = models.IntegerField(blank=True, null=True)
    seisan = models.DateField(blank=True, null=True)
    om = models.CharField(max_length=50, blank = True)
    banch = models.CharField(max_length=50, blank=True, null=True)

    def __str__(self):
        return self.om

class LocStatus(models.Model):
    koshinbi = models.DateField(blank=True, null=True)
    shijibi = models.CharField(max_length=50, blank = True)

    def __str__(self):
        return self.koshinbi

class Kakutei(models.Model):
    code = models.TextField(blank=True, null=True)
    qty = models.IntegerField(blank=True, null=True)
    loc_qty = models.IntegerField(blank=True, null=True)
    seisan = models.DateField(blank=True, null=True)
    om = models.CharField(max_length=50, blank = True)
    banch = models.CharField(max_length=50, blank=True, null=True)

    def __str__(self):
        return self.code + '.' + str(self.qty) + ':' + self.banch + ':' + self.om


class Addcover(models.Model):
    hcode = models.TextField(blank=True, null=True)
    qty = models.FloatField(blank=True, null=True)
    invn = models.TextField(blank=True, null=True)

#しまうための、[番地、コード、数量、既存数] 
#整理用リスト兼追加リスト
class Input(models.Model):
    banch = models.CharField(max_length=50, blank=True, null=True)
    hcode = models.TextField(blank=True, null=True)
    qty = models.FloatField(blank=True, null=True)
    kqty = models.FloatField(blank=True, null=True)

#仕入先コードリスト
class Shiire(models.Model):
    scode = models.CharField(max_length=30)
    sname = models.CharField(max_length=200)

    def __str__(self):
        return self.scode

#背番号リスト
class Bango(models.Model):
    hcode = models.CharField(max_length=200)
    se = models.CharField(max_length=30, unique=True)
    shiire = models.ForeignKey(Shiire, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return self.se
