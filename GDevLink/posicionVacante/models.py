from django.db import models
from usuarios.models import Usuario
from proyectos.models import Proyecto
from django.contrib.postgres.fields import ArrayField
from main.enum import PosiblesRoles, PosiblesFrameworks

class PosicionVacante(models.Model): 
    roles = ArrayField(models.CharField(blank=False, choices=PosiblesRoles.choices, max_length=2),null = True)
    frameworks = ArrayField(models.CharField(blank=False, choices=PosiblesFrameworks.choices, max_length=2),null = True)
    descripcion = models.CharField(max_length=500, blank=True)
    aplicantes = models.ManyToManyField('usuarios.Usuario', blank=True, related_name="aplicantes")
    proyecto = models.ForeignKey('proyectos.Proyecto',on_delete=models.CASCADE,related_name='vacantes',blank=False,null=False)