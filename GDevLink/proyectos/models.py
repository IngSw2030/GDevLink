from django.db import models
from django.contrib.postgres.fields import ArrayField
from usuarios.models import Usuario
from main.enum import PosiblesFases, PosiblesPermisos, PosiblesRoles, PosiblesGeneros, PosiblesFrameworks

class Proyecto(models.Model):
    nombre = models.CharField(max_length=50, blank=False, null=False)
    generos = ArrayField(models.CharField(choices=PosiblesGeneros.choices, max_length=10),blank=False,null=False)
    fase = models.CharField(blank=False, choices=PosiblesFases.choices, max_length=10,null=False)
    descripcion = models.CharField(max_length=500, blank=True,null=True)
    frameworks = ArrayField(models.CharField(choices=PosiblesFrameworks.choices, max_length=10),blank=False,null=False)
    imagen = models.ImageField(upload_to='proyectos',blank=True,null=True)
    enlace_video = models.CharField(max_length=500, blank=True, null=True)
    enlace_juego = models.CharField(max_length=500, blank=True, null=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    seguidores = models.ManyToManyField('usuarios.Usuario', blank=True, related_name="proyectos_seguidos")
    def numero_seguidores(self):
        return self.seguidores.all().count()

class Participacion(models.Model):
    usuario = models.ForeignKey('usuarios.Usuario',on_delete=models.CASCADE,related_name='participaciones',blank=False,null=False)
    proyecto = models.ForeignKey('Proyecto',on_delete=models.CASCADE,related_name='participaciones',blank=False,null=False)
    roles = ArrayField(models.CharField(choices=PosiblesRoles.choices, max_length=10),blank=False,null=False)
    permiso = models.CharField(blank=False, choices=PosiblesPermisos.choices, max_length=10,null=False)

class Actualizacion(models.Model):
    proyecto = models.ForeignKey('Proyecto',on_delete=models.CASCADE,related_name='actualizaciones',blank=False,null=False)
    fecha = models.DateTimeField(auto_now_add=True)
    descripcion = models.CharField(max_length=500, blank=False,null=False)
    imagen = models.ImageField(upload_to='actualizaciones',blank=True,null=True)
