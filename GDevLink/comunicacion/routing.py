from django.urls import path, re_path
from channels.routing import ProtocolTypeRouter, URLRouter
from .consumers import ChatConsumer
from django.conf.urls import url


websockets = URLRouter([
  re_path(r'^ws/comunicacion/conversaciones/(?P<room_name>[^/]+)/chat/', ChatConsumer.as_asgi())
])