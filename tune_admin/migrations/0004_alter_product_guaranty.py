# Generated by Django 3.2.12 on 2022-05-03 14:20

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('tune_admin', '0003_alter_product_state'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='guaranty',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='tune_admin.guarantymodel', verbose_name='Гарантия'),
        ),
    ]
