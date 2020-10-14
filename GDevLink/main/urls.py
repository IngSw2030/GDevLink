from django.urls import path
from . import views
from django.conf.urls import include

urlpatterns = [
    path("layout", views.layout, name="layout"),
    path("", views.index, name="index"),
    path('login', include(('usuarios.urls', 'vista_login'), namespace='usuarios')),
    path('logout', include(('usuarios.urls', 'logout'), namespace='usuarios'))
]