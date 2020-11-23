#Interfaz del manejador de comunicación
class IManejadorComunicacion:
    #Método que retorna las conversaciones del usuario cuyo nombre de usuario
    #es pasado como parámetro. En caso de que el usuario no exista, se
    #retorna None
    def obtenerConversaciones(nombreUsuario):
        pass

    #Método que retorna la conversación cuyo id es pasado como parámetro.
    #También se recibe como parámetro el nombre de usuario del que
    #solicita ver la conversación. En caso de que el usuario solicitante
    #no sea uno de los participantes de la conversación, o que el usuario
    #o la conversacion especificados no existean, se retorna None.
    def obtenerMensajes(nombreUsuario, idConversacion):
        pass

    #Método que crea una conversación entre los dos usuarios cuyos nombres
    #de usuario son pasados como parámetro. Si la conversación se crea
    #correctamente, se retorna la nueva conversación. En caso de que
    #haya ocurrido un error durante la creación de la conversación,
    #se retorna None. Si la conversación ya existe, esta es retornada.
    def agregarConversacion(nombreUsuario1, nombreUsuario2):
        pass