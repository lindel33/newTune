# Generated by Django 3.2.12 on 2022-04-27 08:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('price', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='AirPods',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('full_names', models.TextField(help_text='AirPods 2, AirPods Pro', verbose_name='Полные названия')),
            ],
            options={
                'verbose_name': 'AirPods',
                'verbose_name_plural': 'AirPods',
            },
        ),
    ]
