# Generated by Django 2.2.16 on 2021-06-08 18:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('po', '0007_auto_20210604_0436'),
    ]

    operations = [
        migrations.AddField(
            model_name='cart',
            name='set',
            field=models.SmallIntegerField(blank=True, null=True, verbose_name='セット品'),
        ),
        migrations.AddField(
            model_name='poline',
            name='set',
            field=models.SmallIntegerField(blank=True, null=True, verbose_name='セット品'),
        ),
    ]
