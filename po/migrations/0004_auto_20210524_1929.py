# Generated by Django 2.2.16 on 2021-05-24 10:29

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('po', '0003_auto_20210524_1924'),
    ]

    operations = [
        migrations.AlterField(
            model_name='poline',
            name='code',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='po.TfcCode'),
        ),
    ]
