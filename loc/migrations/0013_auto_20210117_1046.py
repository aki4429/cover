# Generated by Django 2.2.16 on 2021-01-17 01:46

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('loc', '0012_input'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Inv',
        ),
        migrations.DeleteModel(
            name='Invline',
        ),
        migrations.DeleteModel(
            name='Po',
        ),
        migrations.DeleteModel(
            name='Poline',
        ),
        migrations.DeleteModel(
            name='TfcCode',
        ),
    ]