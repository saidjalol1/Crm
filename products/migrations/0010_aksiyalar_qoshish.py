# Generated by Django 4.2.7 on 2023-12-10 13:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0009_remove_product_old_price'),
    ]

    operations = [
        migrations.CreateModel(
            name='Aksiyalar_qoshish',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('description', models.TextField()),
                ('date_added', models.DateTimeField(auto_now_add=True)),
                ('image', models.ImageField(upload_to='aksiyalar_rasmlari/')),
            ],
        ),
    ]
