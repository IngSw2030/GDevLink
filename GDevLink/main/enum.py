from django.db import models
from django.utils.translation import gettext_lazy as _

class PosiblesRoles(models.TextChoices):
        PROGRAMADOR = 'PR', _('Programador')
        DIRECTOR = 'DI', _('Director')
        ARTISTA = 'AR', _('Artista')
        PRODUCTOR = 'PD', _('Productor')
        DISENADOR = 'DS', _('Diseñador')

class PosiblesGeneros(models.TextChoices):
        PLATAFORMA = 'PL', _('Plataforma')
        PELEA = 'PE', _('Pelea')
        SHOOTER = 'SH', _('Shooter')
        RPG = 'RP', _('RPG')
        CARRERAS = 'CA', _('Carreras')

class PosiblesFrameworks(models.TextChoices):
        UNITY = 'UN', _('Unity')
        UNREAL = 'UR', _('Unreal Engine')

class PosiblesFases(models.TextChoices):
        PROGRAMADOR = 'PL', _('Planeación')
        PREPRODUCCION = 'PP', _('Pre-producción')
        PRODUCCION = 'PR', _('Producción')
        PRUEBAS = 'PU', _('Pruebas')
        POSTPRODUCCION = 'PO', _('Post-producción')

class PosiblesPermisos(models.TextChoices):
        MIEMBRO = 'MI', _('Miembro')
        ADMIN = 'AD', _('Administrador')
        MASTER = 'MA', _('Administrador maestro')