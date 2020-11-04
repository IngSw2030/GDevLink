from django.db import models
from usuarios.models import Usuario

# Create your models here.
class Pregunta(models.Model):
    titulo = models.CharField(max_length=50, blank=False, null=False)
    texto =  models.CharField(max_length=1000, blank=True,null=True)
    autor = models.ForeignKey('usuarios.Usuario',on_delete=models.CASCADE,related_name='preguntas',blank=False,null=False)
    mejorRespuesta = models.ForeignKey('Respuesta',on_delete=models.CASCADE,related_name='mejorRespuesta',blank=True,null=True)
    puntosPositivos = models.ForeignKey('usuarios.Usuario',on_delete=models.CASCADE,related_name='preguntasPuntosPositivos',blank=True,null=True)
    puntosNegativos = models.ForeignKey('usuarios.Usuario',on_delete=models.CASCADE,related_name='preguntasPuntosNegativos',blank=True,null=True)

class Respuesta(models.Model):
    pregunta = models.ForeignKey('Pregunta',on_delete=models.CASCADE,related_name='respuestas',blank=False,null=False)
    texto =  models.CharField(max_length=1000, blank=True,null=True)
    autor = models.ForeignKey('usuarios.Usuario',on_delete=models.CASCADE,related_name='respuestas',blank=False,null=False)
    puntosPositivos = models.ForeignKey('usuarios.Usuario',on_delete=models.CASCADE,related_name='respuestasPuntosPositivos',blank=True,null=True)
    puntosNegativos = models.ForeignKey('usuarios.Usuario',on_delete=models.CASCADE,related_name='resouestasPuntosNegativos',blank=True,null=True)