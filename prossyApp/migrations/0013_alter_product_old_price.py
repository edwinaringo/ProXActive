# Generated by Django 4.2.7 on 2023-11-18 07:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('prossyApp', '0012_alter_product_old_price'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='old_price',
            field=models.DecimalField(blank=True, decimal_places=2, default='1500.00', max_digits=999999999, null=True),
        ),
    ]
