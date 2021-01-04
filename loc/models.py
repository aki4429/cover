from django.db import models
from django.conf import settings

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
    file_name = models.FileField(upload_to='shiji/')
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
        return self.code + '.' + self.qty + ':' + self.banch + ':' + self.om


# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey has `on_delete` set to the desired behavior.
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.

class TfcCode(models.Model):
    hinban = models.TextField(blank=True, null=True)
    item = models.TextField(blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    remarks = models.TextField(blank=True, null=True)
    unit = models.TextField(blank=True, null=True)
    uprice = models.TextField(blank=True, null=True)
    ouritem = models.TextField(blank=True, null=True)
    vol = models.TextField(blank=True, null=True)
    zaiko = models.TextField(blank=True, null=True)
    kento = models.TextField(blank=True, null=True)
    hcode = models.TextField(blank=True, null=True)
    cat = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'tfc_code'


class Po(models.Model):
    pod = models.TextField(blank=True, null=True)
    pon = models.TextField(blank=True, null=True)
    per = models.TextField(blank=True, null=True)
    port = models.TextField(blank=True, null=True)
    shipto = models.TextField(blank=True, null=True)
    etd = models.TextField(db_column='ETD', blank=True, null=True)  # Field name made lowercase.
    comment = models.TextField(blank=True, null=True)
    delivery = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'po'



class Poline(models.Model):
    code = models.ForeignKey(TfcCode, on_delete=models.PROTECT)
    remark = models.TextField(blank=True, null=True)
    om = models.IntegerField(blank=True, null=True)
    qty = models.FloatField(blank=True, null=True)
    balance = models.FloatField(blank=True, null=True)
    po = models.ForeignKey(Po, on_delete=models.PROTECT)

    class Meta:
        managed = False
        db_table = 'poline'

class Inv(models.Model):
    invn = models.TextField(blank=True, null=True)
    etd = models.TextField(blank=True, null=True)
    delivery = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'inv'


class Invline(models.Model):
    code = models.ForeignKey(TfcCode, on_delete=models.PROTECT)
    qty = models.FloatField(blank=True, null=True)
    minashi = models.FloatField(blank=True, null=True)
    inv = models.ForeignKey(Inv, on_delete=models.PROTECT)
    poline = models.ManyToManyField(Poline)
    item = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'invline'


class Addcover(models.Model):
    hcode = models.TextField(blank=True, null=True)
    qty = models.FloatField(blank=True, null=True)
    invn = models.TextField(blank=True, null=True)

