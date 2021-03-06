from django.contrib.auth.models import AbstractUser
from django.db import models
from django.contrib.postgres.fields import ArrayField
from main.enum import Framework, Genero, Rol



class Usuario(AbstractUser): 
    roles = ArrayField(models.CharField(blank=False, choices=Rol.choices, max_length=2),null = True)
    generos = ArrayField(models.CharField(blank=False, choices=Genero.choices, max_length=2),null = True)
    frameworks = ArrayField(models.CharField(blank=False, choices=Framework.choices, max_length=2),null = True)
    descripcion = models.CharField(max_length=500, blank=True)
    imagen = models.ImageField(upload_to='usuarios',blank=True)
 