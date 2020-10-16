from django.urls import path
from . import views

urlpatterns = [
    path("crearProyecto", views.crearProyecto,name="crearProyecto"),
    path("UProyectos",views.proyectosUsuario,name="misProyectos"),
    path("proyecto/<str:nombre>",views.proyecto,name="proyecto")
]