# Generated by Django 4.0.6 on 2022-11-22 01:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('transportesEscolaresSena', '0006_alter_vehiculo_color'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='servicios',
            name='tipo_serv',
        ),
        migrations.AddField(
            model_name='servicios',
            name='caracteristicas',
            field=models.CharField(default=1, max_length=500),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='vehiculo',
            name='foto',
            field=models.ImageField(default='transportes/fotos/default.webp', upload_to='transportes/fotos'),
        ),
        migrations.DeleteModel(
            name='TiposdeServicios',
        ),
    ]
