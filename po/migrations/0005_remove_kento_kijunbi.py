# Generated by Django 2.2.16 on 2021-05-24 15:01

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('po', '0004_auto_20210524_1929'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='kento',
            name='kijunbi',
        ),
    ]