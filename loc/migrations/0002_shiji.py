# Generated by Django 2.2.16 on 2020-09-20 04:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('loc', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Shiji',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('file_name', models.CharField(blank=True, max_length=255)),
                ('seisan_shiji', models.FileField(upload_to='shiji/')),
                ('uploaded_at', models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]