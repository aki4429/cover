from django.db import models

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
