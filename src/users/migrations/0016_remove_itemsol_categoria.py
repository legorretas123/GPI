# Generated by Django 2.0.5 on 2018-08-13 02:03

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0015_materialabstracto_categoria'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='itemsol',
            name='categoria',
        ),
    ]
