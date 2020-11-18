from django.urls import path
from . import views
from django.conf.urls import include

urlpatterns = [
    path("conversaciones", views.conversaciones, name="conversaciones"),
    path("chat/<str:room_name>/", views.chat, name="chat")
]