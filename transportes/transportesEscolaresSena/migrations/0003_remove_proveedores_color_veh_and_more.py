# Generated by Django 4.0.6 on 2022-10-31 15:11

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('transportesEscolaresSena', '0002_cliente_clave_cliente_rol_cliente_usuario_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='proveedores',
            name='color_veh',
        ),
        migrations.RemoveField(
            model_name='proveedores',
            name='documentacion_veh',
        ),
        migrations.RemoveField(
            model_name='proveedores',
            name='marca_veh',
        ),
        migrations.CreateModel(
            name='Vehiculo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('placa', models.CharField(max_length=100)),
                ('marca', models.CharField(max_length=100)),
                ('color', models.EmailField(max_length=250)),
                ('foto', models.IntegerField()),
                ('proveedor', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='transportesEscolaresSena.proveedores')),
            ],
        ),
    ]
