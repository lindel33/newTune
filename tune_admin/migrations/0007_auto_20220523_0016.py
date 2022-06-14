# Generated by Django 3.2.12 on 2022-05-23 00:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tune_admin', '0006_auto_20220523_0013'),
    ]

    operations = [
        migrations.AddField(
            model_name='usermodel',
            name='name',
            field=models.CharField(default=1, max_length=90, verbose_name='Ник'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='usermodel',
            name='first_name',
            field=models.CharField(max_length=90, verbose_name='Имя'),
        ),
        migrations.AlterField(
            model_name='usermodel',
            name='last_name',
            field=models.CharField(max_length=90, verbose_name='Фамилия'),
        ),
    ]
