from django.urls import path, include
from . import views

urlpatterns = [
    path("login", views.vista_login, name="login"),
    path("logout", views.vista_logout, name="logout"),
    path("registrar", views.registrar, name="registrar"),
    path("perfil/<str:nombre_usuario>", views.perfil, name="perfil"),
    path("editar/<str:nombre_usuario>", views.editar, name="editar"),
    path('accounts/', include('allauth.urls')),
    path("cambiarClave", views.cambiarClave, name="cambiarClave"),

]