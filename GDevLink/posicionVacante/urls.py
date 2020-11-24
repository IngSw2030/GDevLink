from django.urls import path
from . import views

urlpatterns = [
    path("", views.vacantes, name="vacantes"),
    path("<str:nombre>/gestion-vacantes", views.gestion_vacantes, name="gestion-vacantes"),
    path("<str:nombre>/gestion-vacantes/creacion", views.nueva_vacante, name="nueva_vacante"),
    path("gestion-vacante/<int:ids>", views.editarVacante, name="editarVacante"),
    path("vacante/<int:ids>", views.vacante, name="vacante"),
    path("gestion-vacante/<int:ids>/aplicantes", views.aplicantes, name="aplicantes"),
    path("explorarVacantes", views.explorarVacantes, name="explorarVacantes"),
]