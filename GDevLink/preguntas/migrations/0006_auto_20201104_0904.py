# Generated by Django 3.1.1 on 2020-11-04 14:04

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('preguntas', '0005_auto_20201103_2056'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='pregunta',
            name='puntosNegativos',
        ),
        migrations.RemoveField(
            model_name='pregunta',
            name='puntosPositivos',
        ),
        migrations.RemoveField(
            model_name='respuesta',
            name='puntosNegativos',
        ),
        migrations.RemoveField(
            model_name='respuesta',
            name='puntosPositivos',
        ),
    ]
