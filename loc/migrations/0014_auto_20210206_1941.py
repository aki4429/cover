# Generated by Django 2.2.16 on 2021-02-06 10:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('loc', '0013_auto_20210117_1046'),
    ]

    operations = [
        migrations.AlterField(
            model_name='shiji',
            name='file_name',
            field=models.FileField(upload_to='shiji/', verbose_name='ファイルを送信'),
        ),
    ]
