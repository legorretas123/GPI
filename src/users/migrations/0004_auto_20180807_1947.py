# Generated by Django 2.0.5 on 2018-08-07 23:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0003_obra_nombre_responsable'),
    ]

    operations = [
        migrations.AlterField(
            model_name='solicitud',
            name='estado',
            field=models.CharField(max_length=30),
        ),
    ]
