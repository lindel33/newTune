# Generated by Django 3.2.12 on 2022-05-02 23:19

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('tune_admin', '0003_alter_product_state'),
        ('provider', '0002_alter_providerproduct_kit'),
    ]

    operations = [
        migrations.AlterField(
            model_name='providerproduct',
            name='state',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='tune_admin.statemodel', verbose_name='Состояние'),
        ),
    ]