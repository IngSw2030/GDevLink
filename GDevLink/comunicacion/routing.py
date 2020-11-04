from django.urls import path, re_path
from channels.routing import ProtocolTypeRouter, URLRouter
from .consumers import ChatConsumer
from django.conf.urls import url


websockets = URLRouter([
  url(r'^ws/comunicacion/chat/(?P<room_name>[^/]+)', ChatConsumer, name="chat")
])