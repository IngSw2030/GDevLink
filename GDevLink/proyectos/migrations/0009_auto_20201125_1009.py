# Generated by Django 3.1.2 on 2020-11-25 15:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('proyectos', '0008_remove_proyecto_galeria'),
    ]

    operations = [
        migrations.AlterField(
            model_name='actualizacion',
            name='descripcion',
            field=models.CharField(max_length=1000),
        ),
        migrations.AlterField(
            model_name='proyecto',
            name='descripcion',
            field=models.CharField(blank=True, max_length=1000, null=True),
        ),
    ]