# Generated by Django 3.2.12 on 2022-05-23 00:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tune_admin', '0008_product_regin'),
    ]

    operations = [
        migrations.AlterField(
            model_name='usermodel',
            name='first_name',
            field=models.CharField(max_length=90, null=True, verbose_name='Имя'),
        ),
        migrations.AlterField(
            model_name='usermodel',
            name='last_name',
            field=models.CharField(max_length=90, null=True, verbose_name='Фамилия'),
        ),
        migrations.AlterField(
            model_name='usermodel',
            name='name',
            field=models.CharField(max_length=90, null=True, verbose_name='Ник'),
        ),
    ]
