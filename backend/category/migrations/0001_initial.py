# Generated by Django 4.2.11 on 2024-03-25 06:58

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, help_text='Введите название категории', max_length=255, null=True, verbose_name='Название категории')),
                ('slug', models.CharField(max_length=100, unique=True, validators=[django.core.validators.RegexValidator(message='В слаге содержится недопустимый символ', regex='^[-a-zA-Z0-9_]+$')], verbose_name='Слаг')),
                ('short_description', models.CharField(blank=True, help_text='Введите краткое описание категории', max_length=255, null=True, verbose_name='Краткое описание категории')),
                ('image', models.ImageField(blank=True, help_text='Загрузите изображение категории', null=True, upload_to='images/categories/', verbose_name='Изображение категории')),
            ],
            options={
                'verbose_name': 'Категория',
                'verbose_name_plural': 'Категории',
            },
        ),
    ]
