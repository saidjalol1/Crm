# Generated by Django 4.2.7 on 2023-12-06 02:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0009_alter_staffs_address'),
    ]

    operations = [
        migrations.AddField(
            model_name='orders',
            name='payment_type',
            field=models.CharField(blank=True, max_length=7, null=True),
        ),
    ]
