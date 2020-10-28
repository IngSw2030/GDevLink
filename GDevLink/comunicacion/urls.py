from django.urls import path
from . import views
from django.conf.urls import include

urlpatterns = [
    path("lobby",views.lobby,name="lobby"),
    path("conversaciones", views.conversaciones, name="conversaciones")
]