from django.urls import path
from . import views

urlpatterns = [
    path("crearProyecto", views.crearProyecto,name="crearProyecto"),
    path("MisProyectos",views.proyectosUsuario,name="MisProyectos"),
    path("proyecto/<str:nombre>",views.proyecto,name="proyecto")
]