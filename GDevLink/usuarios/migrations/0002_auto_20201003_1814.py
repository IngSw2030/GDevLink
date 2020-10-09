# Generated by Django 3.1.2 on 2020-10-03 23:14

import django.contrib.postgres.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('usuarios', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='usuario',
            name='frameworks',
            field=django.contrib.postgres.fields.ArrayField(base_field=models.CharField(blank=True, choices=[('UN', 'Unity'), ('UR', 'Unreal Engine')], max_length=2), size=None),
        ),
        migrations.AlterField(
            model_name='usuario',
            name='generos',
            field=django.contrib.postgres.fields.ArrayField(base_field=models.CharField(blank=True, choices=[('PL', 'Plataforma'), ('PE', 'Pelea'), ('SH', 'Shooter'), ('RP', 'RPG'), ('CA', 'Carreras')], max_length=2), size=None),
        ),
        migrations.AlterField(
            model_name='usuario',
            name='roles',
            field=django.contrib.postgres.fields.ArrayField(base_field=models.CharField(blank=True, choices=[('PR', 'Programador'), ('DI', 'Director'), ('AR', 'Artista'), ('PD', 'Productor'), ('DS', 'Diseñador')], max_length=2), size=None),
        ),
    ]
