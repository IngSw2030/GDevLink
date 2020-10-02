from django.contrib.auth.models import AbstractUser
from django.db import models
from django.contrib.postgres.fields import ArrayField

class User(AbstractUser):
    PosiblesRoles = models.TextChoices('PosiblesRoles', 'Programador Director Artista Productor')
    PosiblesGeneros = models.TextChoices('PosiblesGeneros','Plataforma Pelea Shooter RPG')
    PosiblesFrameworks = models.TextChoices('PosiblesFrameworks','Unity UnrealEngine')
    
    roles = ArrayField(models.CharField(blank=False, choices=PosiblesRoles.choices, max_length=20))
    generos = ArrayField(models.CharField(blank=False, choices=PosiblesGeneros.choices, max_length=20))
    frameworks = ArrayField(models.CharField(blank=False, choices=PosiblesFrameworks.choices, max_length=20))
    descripcion = models.CharField(max_length=500, blank=True)