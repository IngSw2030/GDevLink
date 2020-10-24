from django.urls import path
from . import views

urlpatterns = [
    path("crearProyecto", views.crearProyecto,name="crearProyecto"),
    path("MisProyectos",views.proyectosUsuario,name="MisProyectos"),
    path("proyecto/<str:nombre>",views.proyecto,name="proyecto"),
    path("editarProyecto/<str:nombre>", views.editarProyecto, name="editarProyecto"),
    path("gestionMiembros/<str:nombre>", views.gestionMiembros, name="gestionMiembros"),
    path("agregarMiembros/<str:nombre>", views.agregarMiembros, name="agregarMiembros"),
    path("eliminarMiembros/<str:nombre>", views.eliminarMiembros, name="eliminarMiembros"),
    path("agregarAdministrador/<str:nombre>", views.agregarAdministrador, name="agregarAdministrador"),
    path("eliminarAdministrador/<str:nombre>", views.eliminarAdministrador, name="eliminarAdministrador")
]