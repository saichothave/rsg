# Generated by Django 5.0.6 on 2024-06-19 09:14

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Brand',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('name', models.CharField(default='Local', max_length=45)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('name', models.CharField(default='No category', max_length=255)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='ProductColor',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('color', models.CharField(default='No Color', max_length=45)),
                ('inventory', models.IntegerField(default=0)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='ProductSize',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('size', models.CharField(default='Free Size', max_length=10)),
                ('inventory', models.IntegerField(default=0)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='SubCategory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('name', models.CharField(default='No sub-category', max_length=255)),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='subcategories', to='inventory.category')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('name', models.CharField(max_length=255)),
                ('image', models.ImageField(blank=True, null=True, upload_to='gallery/products')),
                ('description', models.TextField()),
                ('buying_price', models.DecimalField(decimal_places=2, max_digits=10)),
                ('selling_price', models.DecimalField(decimal_places=2, max_digits=10)),
                ('applicable_gst', models.DecimalField(decimal_places=2, max_digits=4)),
                ('inventory', models.IntegerField(default=0)),
                ('hsn_code', models.CharField(blank=True, max_length=20, null=True)),
                ('qr_code', models.CharField(blank=True, max_length=20, null=True, unique=True)),
                ('barcode', models.CharField(blank=True, max_length=100, null=True, unique=True)),
                ('brand', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='models', to='inventory.brand')),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='products', to='inventory.category')),
                ('color', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='inventory.productcolor')),
                ('size', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='inventory.productsize')),
                ('subcategory', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='products', to='inventory.subcategory')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
