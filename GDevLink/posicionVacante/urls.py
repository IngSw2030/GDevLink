from django.urls import path
from . import views

urlpatterns = [
    path("", views.explorarVacantes, name="vacantes"),
    path("<str:nombre>/gestion-vacantes", views.gestion_vacantes, name="gestion-vacantes"),
    path("<str:nombre>/gestion-vacantes/creacion", views.nueva_vacante, name="nueva_vacante"),
    path("gestion-vacante/<int:ids>", views.editarVacante, name="editarVacante"),
    path("vacante/<int:ids>", views.vacante, name="vacante"),
    path("vacante/<int:ids>/aplicantes", views.aplicantes, name="aplicantes"),
    path("vacante/<int:ids>/listaAplicantes", views.listaAplicantes, name="listaAplicantes")
]