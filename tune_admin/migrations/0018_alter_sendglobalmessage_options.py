# Generated by Django 3.2.12 on 2022-06-14 05:07

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tune_admin', '0017_alter_product_name'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='sendglobalmessage',
            options={'verbose_name': 'Рассылка', 'verbose_name_plural': 'Рассылка'},
        ),
    ]