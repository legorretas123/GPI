# Generated by Django 2.0.5 on 2018-08-12 23:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0008_auto_20180808_0902'),
    ]

    operations = [
        migrations.AddField(
            model_name='materialreal',
            name='caracteristicas',
            field=models.CharField(blank=True, max_length=100),
        ),
    ]