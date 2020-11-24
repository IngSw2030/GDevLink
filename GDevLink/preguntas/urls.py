from django.urls import path
from . import views


urlpatterns = [
    path("",views.preguntas,name="preguntas"),
    path("creacion",views.crearPregunta,name="crearPregunta"),
    path("pregunta/<int:ids>",views.verPregunta,name="verPregunta"),
    path("pregunta/<int:ids>/respuestas",views.crearRespuesta,name="crearRespuesta"),
    path("pregunta/<int:ids>/puntos-positivos",views.puntuarPreguntaPos,name="puntuarPreguntaPos"),
    path("pregunta/<int:ids>/puntos-negativos",views.puntuarPreguntaNeg,name="puntuarPreguntaNeg"),
    path("pregunta/<int:ids>/mejor-respuesta",views.seleccionarMejorRespuesta,name="seleccionarMejorRespuesta"),
    path("respuesta/<int:ids>/puntos-positivos",views.puntuarRespuestaPos,name="puntuarRespuestaPos"),
    path("respuesta/<int:ids>/puntos-negativos",views.puntuarRespuestaNeg,name="puntuarRespuestaNeg"),
]