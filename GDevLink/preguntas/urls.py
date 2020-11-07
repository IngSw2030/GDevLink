from django.urls import path
from . import views


urlpatterns = [
    path("preguntas",views.preguntas,name="preguntas"),
    path("crearPregunta",views.crearPregunta,name="crearPregunta"),
    path("verPregunta/<int:ids>",views.verPregunta,name="verPregunta"),
    path("crearRespuesta/<int:ids>",views.crearRespuesta,name="crearRespuesta"),
    path("puntuarPreguntaPos/<int:ids>",views.puntuarPreguntaPos,name="puntuarPreguntaPos"),
    path("puntuarPreguntaNeg/<int:ids>",views.puntuarPreguntaNeg,name="puntuarPreguntaNeg"),
    path("seleccionarMejorRespuesta/<int:ids>",views.seleccionarMejorRespuesta,name="seleccionarMejorRespuesta"),
    path("puntuarRespuestaPos/<int:ids>",views.puntuarRespuestaPos,name="puntuarRespuestaPos"),
    path("puntuarRespuestaNeg/<int:ids>",views.puntuarRespuestaNeg,name="puntuarRespuestaNeg"),
]