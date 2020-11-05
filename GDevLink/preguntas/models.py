from django.db import models
from usuarios.models import Usuario
from django.contrib.postgres.fields import ArrayField

# Create your models here.
class Pregunta(models.Model):
    titulo = models.CharField(max_length=50, blank=False, null=False)
    texto =  models.CharField(max_length=1000, blank=True,null=True)
    autor = models.ForeignKey('usuarios.Usuario',on_delete=models.CASCADE,related_name='preguntas',blank=False,null=False)
    mejorRespuesta = models.ForeignKey('Respuesta',on_delete=models.CASCADE,related_name='mejorRespuesta',blank=True,null=True)
    puntosPositivos =models.ManyToManyField('usuarios.Usuario', blank=True, related_name="preguntasPuntosPositivos")
    puntosNegativos =models.ManyToManyField('usuarios.Usuario', blank=True, related_name="preguntasPuntosNegativos")
    def puntos_positivos(self):
        return self.puntosPositivos.all().count()
    def puntos_negativos(self):
        return self.puntosNegativos.all().count()

class Respuesta(models.Model):
    pregunta = models.ForeignKey('Pregunta',on_delete=models.CASCADE,related_name='respuestas',blank=False,null=False)
    texto =  models.CharField(max_length=1000, blank=True,null=True)
    autor = models.ForeignKey('usuarios.Usuario',on_delete=models.CASCADE,related_name='respuestas',blank=False,null=False)
    puntosPositivos =models.ManyToManyField('usuarios.Usuario', blank=True, related_name="respuestasPuntosPositivos")
    puntosNegativos =models.ManyToManyField('usuarios.Usuario', blank=True, related_name="respuestasPuntosNegativos")
    def puntos_positivos(self):
        return self.puntosPositivos.all().count()
    def puntos_negativos(self):
        return self.puntosNegativos.all().count()