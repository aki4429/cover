from django.db import models

class TfcCode(models.Model):
    ZAIKO_CHOICES = (
    (0, '在庫管理なし'),
    (1, '在庫管理あり'),)

    KENTO_CHOICES = (
    (0, '発注管理なし'),
    (1, '発注管理あり'),)

    UNIT_CHOICES = (
    ('pcs','PCS'),
    ('set','SET'),
    ('M','M'),)

    hinban = models.TextField(blank=True, null=True, max_length=100, verbose_name="品番")
    item = models.TextField(blank=True, null=True, max_length=100, verbose_name="アイテム")
    description = models.TextField(blank=True, null=True, max_length=100, verbose_name="詳細")
    remarks = models.TextField(blank=True, null=True, max_length=100, verbose_name="備考")
    unit = models.TextField(blank=True, null=True, max_length=20, choices = UNIT_CHOICES, verbose_name="単位")
    uprice = models.TextField(blank=True, null=True, max_length=40, verbose_name="単価")
    ouritem = models.TextField(blank=True, null=True)
    vol = models.TextField(blank=True, null=True, max_length=10, verbose_name="容積")
    zaiko = models.IntegerField(blank=True, null=True, verbose_name="在庫管理", choices = ZAIKO_CHOICES)
    kento = models.IntegerField(blank=True, null=True, verbose_name="発注管理", choices = KENTO_CHOICES)
    hcode = models.TextField(blank=True, null=True, max_length=100, verbose_name="フクラ品番")
    cat = models.TextField(blank=True, null=True, max_length=20, verbose_name="分類")

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

class Juchu(models.Model):
    file_name = models.FileField(upload_to='juchu/')
    uploaded_at = models.DateTimeField(auto_now_add=True)
