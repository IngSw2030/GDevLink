from django.urls import path
from . import views


urlpatterns = [
    path("preguntas",views.preguntas,name="preguntas"),
    path("crearPregunta",views.crearPregunta,name="crearPregunta"),
    path("verPregunta/<int:ids>",views.verPregunta,name="verPregunta"),
    path("crearRespuesta/<int:ids>",views.crearRespuesta,name="crearRespuesta"),
]