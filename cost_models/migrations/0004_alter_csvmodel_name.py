# Generated by Django 3.2.12 on 2022-06-21 21:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cost_models', '0003_alter_csvmodel_cost'),
    ]

    operations = [
        migrations.AlterField(
            model_name='csvmodel',
            name='name',
            field=models.TextField(verbose_name='Название товара'),
        ),
    ]
