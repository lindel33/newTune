# Generated by Django 3.2.12 on 2022-05-23 00:19

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('tune_admin', '0007_auto_20220523_0016'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='regin',
            field=models.ForeignKey(default=1, null=True, on_delete=django.db.models.deletion.CASCADE, to='tune_admin.regionusermodel', verbose_name='Регион'),
        ),
    ]
