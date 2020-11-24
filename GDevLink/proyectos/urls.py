from django.urls import path
from . import views

urlpatterns = [
    path("", views.explorarProyectos, name="explorarProyectos"),
    path("creacion", views.crearProyecto,name="crearProyecto"),
    path("mis-proyectos",views.proyectosUsuario,name="MisProyectos"),
    path("<str:nombre>/proyecto",views.proyecto,name="proyecto"),
    path("<str:nombre>/edicion", views.editarProyecto, name="editarProyecto"),
    path("<str:nombre>/gestion-miembros", views.gestionMiembros, name="gestionMiembros"),
    path("<str:nombre>/actualizaciones", views.nuevaActualizacion, name="nuevaActualizacion"),
    path("<str:nombre>/seguidores", views.seguir, name="seguir"),
    path("<str:nombre>/administradores", views.administradores, name="administradores"),
    path("<str:nombre>/miembros", views.miembros, name="miembros"),
]