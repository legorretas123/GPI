# Generated by Django 2.0.5 on 2018-08-07 22:06

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import users.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Bodega',
            fields=[
                ('bodega_id', models.AutoField(primary_key=True, serialize=False)),
                ('nombre', models.CharField(blank=True, max_length=100)),
                ('ubicacion', models.CharField(blank=True, max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Itemsol',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cantidad_pedida', models.IntegerField()),
                ('estado', models.CharField(max_length=30)),
            ],
        ),
        migrations.CreateModel(
            name='MaterialAbstracto',
            fields=[
                ('nombre', models.CharField(max_length=100, primary_key=True, serialize=False)),
            ],
        ),
        migrations.CreateModel(
            name='MaterialReal',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('marca', models.CharField(max_length=100)),
                ('codigo', models.CharField(blank=True, max_length=100)),
                ('cantidad', models.IntegerField()),
                ('bodega', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='users.Bodega')),
                ('material', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='users.MaterialAbstracto')),
            ],
        ),
        migrations.CreateModel(
            name='Obra',
            fields=[
                ('nombre', models.CharField(max_length=100, primary_key=True, serialize=False)),
                ('ubicacion', models.CharField(max_length=100)),
                ('email', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Odecompra',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('estado', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tipo', models.CharField(choices=[('B', 'Bodeguero'), ('E', 'Encargado de compras'), ('C', 'Centro de negocios')], default='', max_length=10)),
                ('avatar', models.ImageField(default='profileM.png', upload_to=users.models.upload_to)),
                ('telefono', models.CharField(max_length=100, null=True)),
                ('activo', models.CharField(default='NO', max_length=4)),
                ('token', models.CharField(default='', max_length=15)),
                ('bodega', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='users.Bodega')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Proveedor',
            fields=[
                ('proveedor_id', models.AutoField(primary_key=True, serialize=False)),
                ('nombre', models.CharField(max_length=100)),
                ('email', models.CharField(max_length=100)),
                ('material', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Solicitud',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fecha', models.DateField()),
                ('estado', models.IntegerField(default=0)),
                ('bodeguero', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='bodeguero', to='users.Profile')),
                ('ecompra', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='ecompra', to='users.Profile')),
                ('obra', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='users.Obra')),
            ],
        ),
        migrations.AddField(
            model_name='odecompra',
            name='ecompra',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='users.Profile'),
        ),
        migrations.AddField(
            model_name='odecompra',
            name='proveedor',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='users.Proveedor'),
        ),
        migrations.AddField(
            model_name='itemsol',
            name='material',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='users.MaterialAbstracto'),
        ),
        migrations.AddField(
            model_name='itemsol',
            name='materialReal',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='users.MaterialReal'),
        ),
        migrations.AddField(
            model_name='itemsol',
            name='oc',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='users.Odecompra'),
        ),
        migrations.AddField(
            model_name='itemsol',
            name='solicitud',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='users.Solicitud'),
        ),
    ]
