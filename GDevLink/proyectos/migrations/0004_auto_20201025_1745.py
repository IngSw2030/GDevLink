# Generated by Django 3.1.1 on 2020-10-25 22:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('proyectos', '0003_auto_20201012_1648'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='actualizacion',
            name='imagenes',
        ),
        migrations.AddField(
            model_name='actualizacion',
            name='imagen',
            field=models.ImageField(blank=True, null=True, upload_to='actualizaciones'),
        ),
    ]
