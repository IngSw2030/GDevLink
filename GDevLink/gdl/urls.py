from django.urls import path
from . import views

app_name = "links"
urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login, name="login"),
    path("registrar", views.registrar, name="registrar")
]