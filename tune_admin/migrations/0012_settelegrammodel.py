# Generated by Django 3.2.12 on 2022-05-25 01:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tune_admin', '0011_bookingproduct_date_sell'),
    ]

    operations = [
        migrations.CreateModel(
            name='SetTelegramModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('flag_test', models.BooleanField()),
            ],
        ),
    ]