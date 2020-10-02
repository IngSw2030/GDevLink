from django.db import models
from django.contrib.postgres.fields import ArrayField
from usuarios.models import Usuario
from main.enum import PosiblesFases, PosiblesPermisos, PosiblesRoles, PosiblesGeneros, PosiblesFrameworks

class Proyecto(models.Model):
    nombre = models.CharField(max_length=50, blank=False)
    generos = ArrayField(models.CharField(blank=False, choices=PosiblesGeneros.choices, max_length=2))
    fase = models.CharField(blank=False, choices=PosiblesFases.choices, max_length=2)
    descripcion = models.CharField(max_length=500, blank=True)
    frameworks = ArrayField(models.CharField(blank=False, choices=PosiblesFrameworks.choices, max_length=2))
    #imagenes
    enlace_video = models.CharField(max_length=500, blank=True)
    enlace_juego = models.CharField(max_length=500, blank=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True)

class Participacion(models.Model):
    usuario = models.ForeignKey('usuarios.Usuario',on_delete=models.CASCADE,related_name='participaciones')
    proyecto = models.ForeignKey('Proyecto',on_delete=models.CASCADE,related_name='participaciones')
    roles = ArrayField(models.CharField(blank=False, choices=PosiblesRoles.choices, max_length=2))
    permiso = models.CharField(blank=False, choices=PosiblesPermisos.choices, max_length=2)

    
