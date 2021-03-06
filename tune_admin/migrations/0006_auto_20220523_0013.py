# Generated by Django 3.2.12 on 2022-05-23 00:13

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('tune_admin', '0005_staticuserhourmodel'),
    ]

    operations = [
        migrations.CreateModel(
            name='RegionUserModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, verbose_name='Регион')),
            ],
            options={
                'verbose_name': 'Регионы',
                'verbose_name_plural': 'Регионы',
            },
        ),
        migrations.AlterField(
            model_name='staticuserhourmodel',
            name='date_created',
            field=models.CharField(max_length=50, verbose_name='Дата создания'),
        ),
        migrations.AlterField(
            model_name='staticuserhourmodel',
            name='full_id',
            field=models.CharField(max_length=50, verbose_name='Ник'),
        ),
        migrations.AlterField(
            model_name='staticuserhourmodel',
            name='user_id',
            field=models.CharField(max_length=50, verbose_name='ID пользователя + час'),
        ),
        migrations.CreateModel(
            name='UserModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user_id', models.CharField(max_length=50, verbose_name='ID пользователя')),
                ('date_created', models.CharField(max_length=50, verbose_name='Дата создания')),
                ('first_name', models.CharField(max_length=90, verbose_name='Ник')),
                ('last_name', models.CharField(max_length=90, verbose_name='Ник')),
                ('super_user', models.BooleanField(default=False, verbose_name='SuperUser')),
                ('region_user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='tune_admin.regionusermodel', verbose_name='Регион')),
            ],
            options={
                'verbose_name': 'Регистрация пользователей',
                'verbose_name_plural': 'Регистрация пользователей',
            },
        ),
    ]
