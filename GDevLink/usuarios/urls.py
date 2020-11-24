from django.urls import path, include
from . import views

urlpatterns = [
    path("inicio-sesion", views.inicio_sesion, name="inicio-sesion"),
    path("cierre-sesion", views.cierre_sesion, name="cierre-sesion"),
    path("registro", views.registro, name="registro"),
    path("<str:nombre_usuario>/perfil", views.perfil, name="perfil"),
    path("<str:nombre_usuario>/perfil/edicion", views.edicion, name="edicion"),
    path('accounts/', include('allauth.urls')),
<<<<<<< HEAD
    path("cambio-clave", views.cambio_clave, name="cambio-clave"),
=======
    path("cambiarClave", views.cambiarClave, name="cambiarClave"),
    path("visitarPerfil/<str:nombre_usuario>", views.visitarPerfil, name="visitarPerfil")

>>>>>>> 1290dc72682045efe2ba8fd18be93a2ad28fe3b9
]