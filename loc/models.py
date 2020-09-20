from django.db import models
from django.conf import settings

# Create your models here.
# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey has `on_delete` set to the desired behavior.
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.


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
    file_name = models.CharField(max_length=255,blank=True)
    seisan_shiji = models.FileField(upload_to='shiji/')
    uploaded_at = models.DateTimeField(auto_now_add=True)
