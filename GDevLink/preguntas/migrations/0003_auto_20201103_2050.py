# Generated by Django 3.1.1 on 2020-11-04 01:50

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('preguntas', '0002_auto_20201103_2049'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='pregunta',
            name='mejorRespuesta',
        ),
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