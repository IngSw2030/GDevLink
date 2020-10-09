from django.contrib.auth.models import AbstractUser
from django.db import models
from django.contrib.postgres.fields import ArrayField
from main.enum import PosiblesFrameworks, PosiblesGeneros, PosiblesRoles



class Usuario(AbstractUser): 
    roles = ArrayField(models.CharField(blank=False, choices=PosiblesRoles.choices, max_length=2),null = True)
    generos = ArrayField(models.CharField(blank=False, choices=PosiblesGeneros.choices, max_length=2),null = True)
    frameworks = ArrayField(models.CharField(blank=False, choices=PosiblesFrameworks.choices, max_length=2),null = True)
    descripcion = models.CharField(max_length=500, blank=True)
    #imagen
 