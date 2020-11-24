from django.urls import path
from . import views

urlpatterns = [
    path("", views.explorarProyectos, name="explorarProyectos"),
    path("crearProyecto", views.crearProyecto,name="crearProyecto"),
    path("MisProyectos",views.proyectosUsuario,name="MisProyectos"),
    path("proyecto/<str:nombre>",views.proyecto,name="proyecto"),
    path("editarProyecto/<str:nombre>", views.editarProyecto, name="editarProyecto"),
    path("gestionMiembros/<str:nombre>", views.gestionMiembros, name="gestionMiembros"),
    path("nuevaActualizacion/<str:nombre>", views.nuevaActualizacion, name="nuevaActualizacion"),
    path("seguir/<str:nombre>", views.seguir, name="seguir"),
    path("promover/<str:nombre>", views.promover, name="promover"),
    path("eliminar/<str:nombre>", views.eliminar, name="eliminar"),
    path("revocar/<str:nombre>", views.revocar, name="revocar") 
]