from django.urls import path
from . import views


urlpatterns = [
    path("preguntas",views.preguntas,name="preguntas")
]