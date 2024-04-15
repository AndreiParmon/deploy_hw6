# Generated by Django 5.0.3 on 2024-04-11 16:42

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Customer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, verbose_name='Имя клиента')),
                ('email', models.EmailField(max_length=254, verbose_name='Почтовый адрес')),
                ('phone_number', models.CharField(max_length=15, verbose_name='Номер телефона')),
                ('address', models.TextField(verbose_name='Адрес')),
                ('registration_date', models.DateField(auto_now_add=True, verbose_name='Дата регистрации')),
            ],
            options={
                'verbose_name': 'Клиент',
                'verbose_name_plural': 'Клиенты',
            },
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, verbose_name='Название')),
                ('description', models.TextField(verbose_name='Описание')),
                ('price', models.DecimalField(decimal_places=2, max_digits=10, verbose_name='Цена')),
                ('quantity', models.IntegerField(verbose_name='Количество')),
                ('added_date', models.DateField(auto_now_add=True, verbose_name='Дата добавления')),
                ('image', models.ImageField(blank=True, default='default_image.png', upload_to='images/', verbose_name='Изображение')),
            ],
            options={
                'verbose_name': 'Товар',
                'verbose_name_plural': 'Товары',
            },
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('total_amount', models.DecimalField(decimal_places=2, default=0.01, max_digits=10, verbose_name='Сумма заказа')),
                ('order_date', models.DateField(auto_now_add=True, verbose_name='Дата заказа')),
                ('customer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='myapp.customer', verbose_name='Клиент')),
                ('products', models.ManyToManyField(to='myapp.product', verbose_name='Товары')),
            ],
            options={
                'verbose_name': 'Заказ',
                'verbose_name_plural': 'Заказы',
            },
        ),
    ]
