from channels.routing import ProtocolTypeRouter, URLRouter
from comunicacion.routing import websockets


application = ProtocolTypeRouter({
  "websocket": websockets,
})