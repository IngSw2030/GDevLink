from django.db import models
from django.contrib.postgres.fields import ArrayField
from usuarios.models import Usuario

# Create your models here.
class Conversacion(models.Model):
    participantes = models.ManyToManyField('usuarios.Usuario',related_name='conversaciones',blank=False,null=False)
    

class Mensaje(models.Model):
    Conversacion = models.ForeignKey('Conversacion',on_delete=models.CASCADE,related_name='mensajes',blank=False,null=False)
    fecha = models.DateTimeField(auto_now_add=True)
    texto = models.CharField(max_length=500, blank=False,null=False)
    autor = models.ForeignKey('usuarios.Usuario',on_delete=models.CASCADE,related_name='mensajes',blank=False,null=False) 