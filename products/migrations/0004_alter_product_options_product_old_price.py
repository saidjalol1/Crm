# Generated by Django 4.2.7 on 2023-11-29 06:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0003_storage_name'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='product',
            options={'ordering': ['id']},
        ),
        migrations.AddField(
            model_name='product',
            name='old_price',
            field=models.IntegerField(default=0),
        ),
    ]
