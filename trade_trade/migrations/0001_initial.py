# Generated by Django 3.2.12 on 2022-05-18 17:22

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Trade',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name_button', models.CharField(max_length=50, verbose_name='Кнопка в боте')),
                ('image_1', models.ImageField(upload_to='', verbose_name='Картинка 1')),
                ('image_2', models.ImageField(upload_to='', verbose_name='Картинка 2')),
                ('text', models.TextField(verbose_name='Текст')),
            ],
            options={
                'verbose_name': 'Обменка',
                'verbose_name_plural': 'Обменки',
            },
        ),
    ]
