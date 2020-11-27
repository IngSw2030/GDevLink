from channels.generic.websocket import AsyncWebsocketConsumer, WebsocketConsumer
from asgiref.sync import async_to_sync
import json
from comunicacion.models import Mensaje, Conversacion
from usuarios.models import Usuario
from comunicacion.ManejadorEnvioMensajes import ManejadorEnvioMensajes

class ChatConsumer(WebsocketConsumer):
    def connect(self):
        self.room_name=self.scope['url_route']['kwargs']['room_name']
        self.room_group_name='chat_%s' % self.room_name

        #Join room group
        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name,
            self.channel_name
        )

        self.accept()

    def disconnect(self, close_code):
        # Leave room group
         print("Desconexion")
         async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name,
            self.channel_name
        )

    # Receive message from WebSocket
    def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        autor = text_data_json['autor']
        
        if ManejadorEnvioMensajes.enviarMensaje(autor, self.room_name, message) == 0:
            # Send message to room group
            async_to_sync (self.channel_layer.group_send)(
                self.room_group_name,
                {
                    'type': 'chat_message',
                    'message': message,
                    'autor': autor
                }
            )
        

    # Receive message from room group
    def chat_message(self, event):
        message = event['message']
        autor = event['autor']
        print("Enviar mensaje")
        self.send(text_data=json.dumps({
            'message': message,
            'autor': autor
        }))