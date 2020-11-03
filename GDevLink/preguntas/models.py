from django.db import models
from usuarios.models import Usuario

# Create your models here.
class Pregunta(models.Model):
    titulo = models.CharField(max_length=50, blank=False, null=False)
    texto =  models.CharField(max_length=1000, blank=True,null=True)
    autor = models.ForeignKey('usuarios.Usuario',on_delete=models.CASCADE,related_name='preguntas',blank=False,null=False)

class Respuesta(models.Model):
    pregunta = models.ForeignKey('Pregunta',on_delete=models.CASCADE,related_name='respuestas',blank=False,null=False)
    texto =  models.CharField(max_length=1000, blank=True,null=True)
    autor = models.ForeignKey('usuarios.Usuario',on_delete=models.CASCADE,related_name='respuestas',blank=False,null=False)