# Generated by Django 2.0.5 on 2018-08-07 22:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='tipo',
            field=models.CharField(choices=[('B', 'Bodeguero'), ('E', 'Compras'), ('C', 'Business')], default='', max_length=10),
        ),
    ]
