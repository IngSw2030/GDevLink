from channels.routing import ProtocolTypeRouter, URLRouter
from comunicacion.routing import websockets


application = ProtocolTypeRouter({
  "websocket": websockets,
})

#application = ProtocolTypeRouter({
    # (http->django views is added by default)
#    'websocket': AuthMiddlewareStack(
#        URLRouter(
#            comunicacion.routing.websockets
#        )
#    ),
#})