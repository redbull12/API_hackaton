# Generated by Django 3.1 on 2021-05-12 14:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0005_like'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='price',
            field=models.DecimalField(decimal_places=0, max_digits=10),
        ),
    ]
