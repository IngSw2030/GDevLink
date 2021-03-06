from comunicacion.IManejadorEnvioMensajes import IManejadorEnvioMensajes
from usuarios.models import Usuario
from comunicacion.models import Mensaje, Conversacion
from usuarios.ManejadorUsuarios import ManejadorUsuarios

#Clase que implementa la interfaz IManejadorEnvioMensajes
class ManejadorEnvioMensajes(IManejadorEnvioMensajes):
    def enviarMensaje(nombreUsuario, idConversacion, texto):
        #Se retorna -1 en caso de que el mensaje esté vacío.
        if texto == '':
            return -1
        #Se obtiene la conversación asociada al id indicado y se retorn -1 en caso de que no exista
        try:
            conversacion = Conversacion.objects.get(id=idConversacion)
        except Conversacion.DoesNotExist:
            return -1
        #Se obtiene asociado al nombre de usuario indicado y se retorna -1 en caso de que no exista
        usuario = ManejadorUsuarios.obtenerUsuario(nombreUsuario)
        if usuario is None:
            return -1
        #Se retorna -1 si el usuario no es participante de la conversación
        if usuario not in conversacion.participantes.all():
            return -1
        #Se crea el mensaje y se guarda en la base de datos
        mensaje = Mensaje.objects.create(Conversacion=conversacion,texto=texto, autor=usuario)
        mensaje.save()
        return 0