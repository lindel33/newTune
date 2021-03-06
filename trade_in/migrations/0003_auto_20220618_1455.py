# Generated by Django 3.2.12 on 2022-06-18 14:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('trade_in', '0002_auto_20220617_0459'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tradeinseriesmodel',
            name='start_cost',
            field=models.IntegerField(default=0, verbose_name='Начальная цена'),
        ),
        migrations.AlterField(
            model_name='variablefoestepmodel',
            name='decrease',
            field=models.IntegerField(default=0, verbose_name='Уменьшение при выборе на'),
        ),
        migrations.AlterField(
            model_name='variablefoestepmodel',
            name='increase',
            field=models.IntegerField(default=0, verbose_name='Увеличение при выборе на'),
        ),
    ]
