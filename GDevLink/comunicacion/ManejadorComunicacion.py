from usuarios.models import Usuario
from comunicacion.IManejadorComunicacion import IManejadorComunicacion
from comunicacion.models import Conversacion, Mensaje
from usuarios.ManejadorUsuarios import ManejadorUsuarios

#Clase que implementa la interfaz IManejadorComunicacion
class ManejadorComunicacion(IManejadorComunicacion):
    def obtenerConversaciones(nombreUsuario):
        #Se obtiene el usuario cuyo nombre de usuario fue recibido como parámetro
        usuario = ManejadorUsuarios.obtenerUsuario(nombreUsuario)
        #Si no se pudo encontrar un usuario con el nombre de usuario especificado,
        #se retorna None
        if usuario is None:
            return None
        #Si el usuario fue encontrado, se retornan sus conversaciones.
        else:
            return usuario.conversaciones.all()

    def obtenerMensajes(nombreUsuario, idConversacion):
        #Se obtiene el usuario cuyo nombre de usuario fue recibido como parámetro
        usuario = ManejadorUsuarios.obtenerUsuario(nombreUsuario)
        #Si el usuario especificado no existe, se retorna None
        if usuario is None:
            return None
        #Se obtiene la conversación asociada al id solicitado
        try:
            conversacion = Conversacion.objects.get(id=idConversacion)
        except Conversacion.DoesNotExist:
            #Si la conversacion no existe, se retorna None
            return None
        #Si el usuario que solicita la conversación es un participante de esta,
        #se retornan todos los mensajes de la conversación.
        if usuario in conversacion.participantes.all():
            return conversacion
        #Si el usuario que solicita la conversación no es un participante de esta,
        #se retorna None
        else:
            return None


    def agregarConversacion(nombreUsuario1, nombreUsuario2):
        #Se obtienen los usuarios especificados
        usuario1 = ManejadorUsuarios.obtenerUsuario(nombreUsuario1)
        usuario2 = ManejadorUsuarios.obtenerUsuario(nombreUsuario2)
        #Si alguno de los usuarios no existe, se retorna None
        if usuario1 is None or usuario2 is None:
            return None
        #Se revisa si ya existe una conversación entre esos dos usuarios
        existente = Conversacion.objects.filter(participantes = usuario1).filter(participantes = usuario2)
        #Si ya existe la conversación, se retorna None
        if existente.count() > 0:
            return existente.all()[0]
        #Se crea una nueva conversación y se agregan los participantes
        conv = Conversacion()
        conv.save()
        conv.participantes.add(usuario1)     
        conv.participantes.add(usuario2)
        conv.save()
        return conv