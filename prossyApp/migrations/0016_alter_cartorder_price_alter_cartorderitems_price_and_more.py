# Generated by Django 4.2.7 on 2023-11-21 10:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('prossyApp', '0015_alter_cartorder_price_alter_cartorderitems_price_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cartorder',
            name='price',
            field=models.DecimalField(decimal_places=2, default='1000.00', max_digits=10),
        ),
        migrations.AlterField(
            model_name='cartorderitems',
            name='price',
            field=models.DecimalField(decimal_places=2, default='1000.00', max_digits=10),
        ),
        migrations.AlterField(
            model_name='cartorderitems',
            name='total',
            field=models.DecimalField(decimal_places=2, default='1000.00', max_digits=10),
        ),
        migrations.AlterField(
            model_name='product',
            name='old_price',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True),
        ),
        migrations.AlterField(
            model_name='product',
            name='price',
            field=models.DecimalField(decimal_places=2, default='1000.00', max_digits=10),
        ),
    ]