from django.urls import path
from . import views

urlpatterns = [
    path("gestionarVacantes/<str:nombre>", views.gestionarVacantes, name="gestionarVacantes"),
    path("nuevaVacante/<str:nombre>", views.nuevaVacante, name="nuevaVacante"),
]