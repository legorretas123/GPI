# Generated by Django 2.0.5 on 2018-08-07 22:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_auto_20180807_1808'),
    ]

    operations = [
        migrations.AddField(
            model_name='obra',
            name='nombre_responsable',
            field=models.CharField(default=None, max_length=100),
        ),
    ]