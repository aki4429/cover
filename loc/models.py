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



