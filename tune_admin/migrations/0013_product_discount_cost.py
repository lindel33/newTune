# Generated by Django 3.2.12 on 2022-06-03 07:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tune_admin', '0012_settelegrammodel'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='discount_cost',
            field=models.PositiveIntegerField(default=0, verbose_name='Цена со скидкой'),
        ),
    ]