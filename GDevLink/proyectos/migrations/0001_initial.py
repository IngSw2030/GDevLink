# Generated by Django 3.1.1 on 2020-10-02 17:36

from django.conf import settings
import django.contrib.postgres.fields
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Proyecto',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=50)),
                ('generos', django.contrib.postgres.fields.ArrayField(base_field=models.CharField(choices=[('PL', 'Plataforma'), ('PE', 'Pelea'), ('SH', 'Shooter'), ('RP', 'RPG'), ('CA', 'Carreras')], max_length=2), size=None)),
                ('fase', models.CharField(choices=[('PL', 'Planeación'), ('PP', 'Pre-producción'), ('PR', 'Producción'), ('PU', 'Pruebas'), ('PO', 'Post-producción')], max_length=2)),
                ('descripcion', models.CharField(blank=True, max_length=500)),
                ('frameworks', django.contrib.postgres.fields.ArrayField(base_field=models.CharField(choices=[('UN', 'Unity'), ('UR', 'Unreal Engine')], max_length=2), size=None)),
                ('enlace_video', models.CharField(blank=True, max_length=500)),
                ('enlace_juego', models.CharField(blank=True, max_length=500)),
                ('fecha_creacion', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='Participacion',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('roles', django.contrib.postgres.fields.ArrayField(base_field=models.CharField(choices=[('PR', 'Programador'), ('DI', 'Director'), ('AR', 'Artista'), ('PD', 'Productor'), ('DS', 'Diseñador')], max_length=2), size=None)),
                ('permiso', models.CharField(choices=[('MI', 'Miembro'), ('AD', 'Administrador'), ('MA', 'Administrador maestro')], max_length=2)),
                ('proyecto', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='participaciones', to='proyectos.proyecto')),
                ('usuario', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='participaciones', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]