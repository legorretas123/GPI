# Generated by Django 2.0.5 on 2018-08-14 12:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0020_auto_20180814_0903'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cotizacion',
            name='proveedor',
            field=models.CharField(default='', max_length=30),
        ),
    ]