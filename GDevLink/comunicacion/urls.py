from django.urls import path
from . import views
from django.conf.urls import include

urlpatterns = [
    path("conversaciones", views.conversaciones, name="conversaciones"),
    path("conversaciones/<str:room_name>/chat/", views.chat, name="chat")
]