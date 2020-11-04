from django.db import models
from usuarios.models import Usuario
from django.contrib.postgres.fields import ArrayField
from main.enum import PosiblesRoles, PosiblesFrameworks

class PosicionVacante(models.Model): 
    roles = ArrayField(models.CharField(blank=False, choices=PosiblesRoles.choices, max_length=2),null = True)
    frameworks = ArrayField(models.CharField(blank=False, choices=PosiblesFrameworks.choices, max_length=2),null = True)
    descripcion = models.CharField(max_length=500, blank=True)
    aplicantes = models.ForeignKey('usuarios.Usuario',on_delete=models.CASCADE,related_name='aplicantes',blank=False,null=False)
    proyecto = models.ForeignKey('Proyecto',on_delete=models.CASCADE,related_name='participaciones',blank=False,null=False)
 