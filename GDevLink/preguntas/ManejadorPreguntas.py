from preguntas.IManejadorPreguntas import IManejadorPreguntas
from preguntas.models import Usuario, Pregunta, Respuesta
from django.db.models import Count
from django.db import IntegrityError

#Clase que implementa la interfaz IManejadorPreguntas
class ManejadorPreguntas(IManejadorPreguntas):
    def obtenerPreguntasPopulares():
        #Se obtienen las preguntas ordenadas por puntos en total
         preguntas=Pregunta.objects.all().annotate(puntos=Count('puntosPositivos') - Count('puntosNegativos')).order_by('-puntos')
         return preguntas

    def crearPregunta(tituloPregunta, textoPregunta, autor):
        #Se recupera el usuario
        usuario=Usuario.objects.get(nombre=autor)
        try:
            #Se crea la pregunta con sus valores iniciales
            pregunta=Pregunta(titulo=tituloPregunta,texto=textoPregunta,autor=usuario)
            pregunta.save()
            respuestas=pregunta.respuestas.all()
            preguntaPos=False
            preguntaNeg=False
            autor=True
            #Se retorna la pregunta
            return pregunta
        except IntegrityError as e:
            #Se retorna None si ocurre un error
            return None

    def verPregunta(idPregunta):
        #Retorno de pregunta que con id o none
        try:
            pregunta=Pregunta.objects.get(id=idPregunta)
            return pregunta
        except Pregunta.DoesNotExist:
            return None

    def responderPregunta(idPregunta, texto, autor):
        try:
            #Creacion de la pregunta con valores iniciales
            respuesta = Respuesta(texto=texto,pregunta=pregunta,autor=request.user)
            respuesta.save()
            return 0
        except IntegrityError as e:
            #Retorno en caso de error
            return 1

    def escogerRespuesta(idRespuesta):
        #Busqueda de pregunta y usuario
        respuesta=Respuesta.objects.get(id=idRespuesta)
        pregunta=respuesta.pregunta
        #Se selecciona la mejor respuesta
        #Si la pregunta ya estaba seleccionada, se le desselecciona
        if pregunta.mejorRespuesta is None:
            pregunta.mejorRespuesta=respuesta
        else:
            if pregunta.mejorRespuesta.id == respuesta.id:
                pregunta.mejorRespuesta=None
            else:
                pregunta.mejorRespuesta=respuesta
        pregunta.save()
        return 0

    def puntuarPreguntaPos(idPregunta, nombreUsuaro):
        #Busqueda de pregunta y usuario
        pregunta=Pregunta.objects.get(id=idPregunta)
        if pregunta is None:
            return 1
        usuario = Usuario.objects.get(username=nombreUsuaro)
        if usuario is None:
            return 1
        #Se le agrega el punto positivo a la pregunta
        #Si la pregunta ya estaba puntuada, se le quita el Punto
        if usuario in pregunta.puntosPositivos.all():
            pregunta.puntosPositivos.remove(usuario)
        else:
            pregunta.puntosPositivos.add(usuario)
        #Si el usuario le habia dado un punto negativo se quita
        if usuario in pregunta.puntosNegativos.all():
            pregunta.puntosNegativos.remove(usuario)
        pregunta.save()
        return 0

    def puntuarPreguntaNeg(idPregunta, nombreUsuaro):
        #Busqueda de pregunta y usuario
        pregunta=Pregunta.objects.get(id=idPregunta)
        if pregunta is None:
            return 1
        usuario = Usuario.objects.get(username=nombreUsuaro)
        if usuario is None:
            return 1
        #Se le agrega el punto negativo a la pregunta
        #Si la pregunta ya estaba puntuada, se le quita el Punto
        if usuario in pregunta.puntosNegativos.all():
            pregunta.puntosNegativos.remove(usuario)
        else:
            pregunta.puntosNegativos.add(usuario)
        #Si el usuario le habia dado un punto poasitivo se quita
        if usuario in pregunta.puntosPositivos.all():
            pregunta.puntosPositivos.remove(usuario)
        pregunta.save()
        return 0

    def puntuarRespuestaPos(idRespuesta, nombreUsuaro):
        #Busqueda de pregunta y usuario
        respuesta=Respuesta.objects.get(id=idRespuesta)
        if respuesta is None:
            return 1
        usuario = Usuario.objects.get(username=nombreUsuaro)
        if usuario is None:
            return 1
        #Se le agrega el punto positivo a la respuesta
        #Si la respuesta ya estaba puntuada, se le quita el Punto
        if usuario in respuesta.puntosPositivos.all():
            respuesta.puntosPositivos.remove(usuario)
        else:
            respuesta.puntosPositivos.add(usuario)
        #Si el usuario le habia dado un punto negativo se quita
        if usuario in respuesta.puntosNegativos.all():
            respuesta.puntosNegativos.remove(usuario)
        respuesta.save()
        return 0

    def puntuarRespuestaNeg(idRespuesta, nombreUsuaro):
        #Busqueda de pregunta y usuario
        respuesta=Respuesta.objects.get(id=idRespuesta)
        if respuesta is None:
            return 1
        usuario = Usuario.objects.get(username=nombreUsuaro)
        if usuario is None:
            return 1
        #Se le agrega el punto negativo a la pregunta
        #Si la respuesta ya estaba puntuada, se le quita el Punto
        if usuario in respuesta.puntosNegativos.all():
            respuesta.puntosNegativos.remove(usuario)
        else:
            respuesta.puntosNegativos.add(usuario)
        #Si el usuario le habia dado un punto positivo se quita
        if usuario in respuesta.puntosPositivos.all():
            respuesta.puntosPositivos.remove(usuario)
        respuesta.save()
        return 0
