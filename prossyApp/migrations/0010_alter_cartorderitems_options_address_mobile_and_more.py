# Generated by Django 4.2.7 on 2023-11-18 07:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('prossyApp', '0009_alter_product_gender'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='cartorderitems',
            options={'verbose_name_plural': 'Cart Order Items'},
        ),
        migrations.AddField(
            model_name='address',
            name='mobile',
            field=models.CharField(max_length=300, null=True),
        ),
        migrations.AlterField(
            model_name='cartorder',
            name='product_status',
            field=models.CharField(choices=[('processing', 'Processing'), ('shipped', 'Shipped'), ('delivered', 'Delivered')], default='processing', max_length=30),
        ),
    ]