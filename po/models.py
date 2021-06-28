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

    def __str__(self):
        return self.hinban

    class Meta:
        managed = True
        db_table = 'tfc_code'


class Condition(models.Model):
    def __str__(self):
        return self.name

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

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'condition'


class Po(models.Model):
    FT40_CHOICES = (
            ('1', '1'),
            ('2', '2'),
            ('3', '3'),
            ('4', '4'),
            ('5', '5'),
            ('6', '6'),
            ('7', '7'),
            ('8', '8'),
            ('9', '9'),
            ('10', '10'),
    )

    FT20_CHOICES = (
            ('1', '1'),
            ('2', '2'),
            ('3', '3'),
            ('4', '4'),
            ('5', '5'),
            ('6', '6'),
            ('7', '7'),
            ('8', '8'),
            ('9', '9'),
            ('10', '10'),
    )

    pod = models.DateField(blank=True, null=True, verbose_name="発注日")
    pon = models.TextField(blank=True, null=True, verbose_name="PO#")
    per = models.TextField(blank=True, null=True, verbose_name="手段")
    port = models.TextField(blank=True, null=True, verbose_name="仕向港")
    shipto = models.TextField(blank=True, null=True, verbose_name="届先")
    etd = models.DateField(db_column='ETD', blank=True, null=True)  # Field name made lowercase.
    comment = models.TextField(blank=True, null=True)
    delivery = models.DateField(blank=True, null=True, verbose_name="取込日")
    condition = models.ForeignKey(Condition, on_delete=models.SET_NULL, blank=True, null=True, default=None)
    ft40 = models.TextField(blank=True, null=True, verbose_name="40f", choices=FT40_CHOICES)
    ft20 = models.TextField(blank=True, null=True, verbose_name="20f", choices=FT20_CHOICES)

    def __str__(self):
        return self.pon

    class Meta:
        managed = True
        db_table = 'po'

class Poline(models.Model):
    #code = models.ForeignKey(TfcCode, on_delete=models.PROTECT)
    code = models.ForeignKey(TfcCode, on_delete=models.SET_NULL, blank= True, null=True )
    remark = models.TextField(blank=True, null=True)
    om = models.TextField(blank=True, null=True)
    qty = models.FloatField(blank=True, null=True)
    balance = models.FloatField(blank=True, null=True)
    #po = models.ForeignKey(Po, on_delete=models.PROTECT)
    po = models.ForeignKey(Po, on_delete=models.SET_NULL, null=True )
    ocode = models.TextField(blank=True, null=True, max_length=100, verbose_name="オービック品番")
    hinmei = models.TextField(blank=True, null=True, max_length=100, verbose_name="オービック商品名")
    kikaku = models.TextField(blank=True, null=True, max_length=100, verbose_name="オービック規格")
    set = models.SmallIntegerField(blank=True, null=True, verbose_name="セット品")
    #並べ替え用に品番から比較ワードを作成
    def hikaku_word(self, hinban):
        word = ''
        if len(hinban.split('-')) > 1 : #モデル名
            word += hinban.split('-')[0]
        if len(hinban.split(' ')) > 1 : #布
            word += hinban.split(' ')[1]
        if len(hinban.split('-')) > 1 : #ピース
            word +=hinban.split('-')[1]
        if len(word) == 0 :
            return hinban
        else:
            return word

    def __lt__(self, other):
        # self < other
        #omの値がNoneだと比較できないので、書き換えておく
        if self.om is None:
            self.om=''
        if other.om is None:
            other.om=''
        if self.om == other.om: #om no.
            if self.om == '':
                return self.code.hcode < other.code.hcode
            else:
                return self.hikaku_word(self.code.hinban) < self.hikaku_word(other.code.hinban)
        else:
            return self.om < other.om

    class Meta:
        managed = True
        db_table = 'poline'

class Inv(models.Model):
    invn = models.TextField(blank=True, null=True, verbose_name="インボイスNo.")
    etd = models.DateField(blank=True, null=True, verbose_name="ETD")
    delivery = models.DateField(blank=True, null=True, verbose_name="取込日")

    def __str__(self):
        return self.invn

    class Meta:
        managed = True
        db_table = 'inv'


class Invline(models.Model):
    code = models.ForeignKey(TfcCode, on_delete=models.SET_NULL, null=True )
    qty = models.FloatField(blank=True, null=True)
    minashi = models.FloatField(blank=True, null=True)
    #inv = models.ForeignKey(Inv, on_delete=models.PROTECT)
    inv = models.ForeignKey(Inv, on_delete=models.CASCADE, null=True)
    #poline = models.ManyToManyField(Poline, null=True, blank=True)
    poline = models.ForeignKey(Poline, on_delete=models.SET_NULL, null=True)
    item = models.TextField(blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'invline'

class Juchu(models.Model):
    file_name = models.FileField(upload_to='juchu/')
    uploaded_at = models.DateTimeField(auto_now_add=True)

class Kento(models.Model):
    file_name = models.FileField(upload_to='kento/')
    uploaded_at = models.DateTimeField(auto_now_add=True)

class Cart(models.Model):
    hinban = models.TextField(blank=True, null=True, max_length=100, verbose_name="品番")
    om = models.TextField(blank=True, null=True)
    juchubi = models.DateField(blank=True, null=True)
    noki = models.DateField(blank=True, null=True)
    qty = models.FloatField(blank=True, null=True)
    flag = models.TextField(blank=True, null=True) #コードがあればok
    obic = models.TextField(blank=True, null=True, max_length=100, verbose_name="オービックコード")
    code = models.ForeignKey(TfcCode, on_delete=models.SET_NULL, null=True )
    hinmei = models.TextField(blank=True, null=True, max_length=100, verbose_name="オービック商品名")
    kikaku = models.TextField(blank=True, null=True, max_length=100, verbose_name="オービック規格")
    set = models.SmallIntegerField(blank=True, null=True, verbose_name="セット品")
    #並べ替え用に品番から比較ワードを作成
    def hikaku_word(self, hinban):
        word = ''
        if len(hinban.split('-')) > 1 : #モデル名
            word += hinban.split('-')[0]
        if len(hinban.split(' ')) > 1 : #布
            word += hinban.split(' ')[1]
        if len(hinban.split('-')) > 1 : #ピース
            word +=hinban.split('-')[1]
        if len(word) == 0 :
            return hinban
        else:
            return word

    def __lt__(self, other):
        # self < other
        if self.om == other.om: #om no.
            return self.hikaku_word(self.hinban) < self.hikaku_word(other.hinban)
        else:
            return self.om < other.om

    class Meta:
        managed = True
        db_table = 'cart'

class Fabric(models.Model):
    code = models.TextField(blank=True, null=True, max_length=100, verbose_name="コード")
    name = models.TextField(blank=True, null=True, max_length=300, verbose_name="名前")

class Shouhi(models.Model):
    month = models.TextField(blank=True, null=True, verbose_name="消費月")
    code = models.TextField(blank=True, null=True, verbose_name="コード")
    qty = models.FloatField(blank=True, null=True, verbose_name="消費数量")


