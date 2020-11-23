#Interfaz del manejador del envío de mensajes
class IManejadorEnvioMensajes:
    #Método que agrega un nuevo mensaje a la conversación cuyo id
    #es indicado. También se recibe como parámetro el usuario que envía
    #el mensaje y el texto del mensaje. En caso de que el usuario no exista,
    #que la conversación no exista, que el usuario no pertenezca a la
    #conversación, o que el texto esté vacío, el mensaje no se envía y
    #se retorna -1. En caso contrario, se retorna 0.
    def enviarMensaje(nombreUsuario, idConversacion, texto):
        pass