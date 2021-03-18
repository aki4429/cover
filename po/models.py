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


class Condition(models.Model):
    SHIP_CHOICES = (
    ('Vessel', 'vessel'),
    ('DHL(Courier)', 'dhl'),
    )

    PORT_CHOICES = (
    ('NAGOYA Port', 'nagoya'),
    ('OSAKA Port', 'osaka'),
    ('HAKATA Port', 'hakata'),
    ('MOJI Port', 'moji'),
    ('Japanese AIR Port', 'air'),
    )

    FORWARDER_CHOICES = (
    ('TRADIA', 'tradia'),
    ('DHL', 'DHL'),
    )

    TRADE_CHOICES = (
    ('FOB Taicang', 'FOB Taicang'),
    ('Ex works', 'Ex Works'),
    ('DDP', 'DDP'),
    )

    PAY_CHOICES = (
    ('Remittance in 30 days each month', 'remittance'),
    ('No Coomercial Value', 'no value'),
    )

    INSURANCE_CHOICES = (
    ('', ''),
    ('to be covered by us', 'to be covered by us'),
    )

    name = models.TextField(blank=True, null=True, max_length=100, verbose_name="輸入形体名")
    shipment_per = models.TextField(blank=True, null=True, choices=SHIP_CHOICES, verbose_name="輸入手段")
    shipto_1 = models.TextField(blank=True, null=True, max_length=100, verbose_name="住所1")
    shipto_2 = models.TextField(blank=True, null=True, max_length=100, verbose_name="住所2")
    shipto_3 = models.TextField(blank=True, null=True, max_length=100, verbose_name="住所3")
    shipto_4 = models.TextField(blank=True, null=True, max_length=100, verbose_name="住所4")
    shipto_5 = models.TextField(blank=True, null=True, max_length=100, verbose_name="住所5")
    via = models.TextField(blank=True, null=True, max_length=50, verbose_name="経由地", choices=PORT_CHOICES)
    forwarder = models.TextField(blank=True, null=True, max_length=50, verbose_name="フォワーダー", choices=FORWARDER_CHOICES)
    trade_term = models.TextField(blank=True, null=True, max_length=50, verbose_name="貿易条件", choices=TRADE_CHOICES)
    payment_term = models.TextField(blank=True, null=True, max_length=50, verbose_name="支払条件", choices=PAY_CHOICES)
    insurance = models.TextField(blank=True, null=True, max_length=50, verbose_name="保険", choices=INSURANCE_CHOICES)
    comment = models.TextField(blank=True, null=True, max_length=100, verbose_name="備考")
    nic = models.TextField(blank=True, null=True, max_length=50, verbose_name="ニックネーム")

    class Meta:
        db_table = 'condition'


class Po(models.Model):
    pod = models.DateField(blank=True, null=True, verbose_name="発注日")
    pon = models.TextField(blank=True, null=True, verbose_name="PO#")
    per = models.TextField(blank=True, null=True, verbose_name="手段")
    port = models.TextField(blank=True, null=True, verbose_name="仕向港")
    shipto = models.TextField(blank=True, null=True, verbose_name="届先")
    etd = models.DateField(db_column='ETD', blank=True, null=True)  # Field name made lowercase.
    comment = models.TextField(blank=True, null=True)
    delivery = models.DateField(blank=True, null=True, verbose_name="取込日")
    condition = models.ForeignKey(Condition, on_delete=models.PROTECT, blank=True, null=True)
    ft40 = models.TextField(blank=True, null=True, verbose_name="40f")
    ft20 = models.TextField(blank=True, null=True, verbose_name="20f")

    class Meta:
        managed = True
        db_table = 'po'

class Poline(models.Model):
    code = models.ForeignKey(TfcCode, on_delete=models.PROTECT)
    remark = models.TextField(blank=True, null=True)
    om = models.TextField(blank=True, null=True)
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


class Cart(models.Model):
    hinban = models.TextField(blank=True, null=True, max_length=100, verbose_name="品番")
    om = models.TextField(blank=True, null=True)
    juchubi = models.DateField(blank=True, null=True)
    noki = models.DateField(blank=True, null=True)
    qty = models.FloatField(blank=True, null=True)
    flag = models.TextField(blank=True, null=True) #コードがあればok
    code = models.TextField(blank=True, null=True) #TfcCodeのｐｋを持つ
    obic = models.TextField(blank=True, null=True, max_length=100, verbose_name="オービックコード")

    class Meta:
        managed = True
        db_table = 'cart'

class Fabric(models.Model):
    code = models.TextField(blank=True, null=True, max_length=100, verbose_name="コード")
    name = models.TextField(blank=True, null=True, max_length=300, verbose_name="名前")

