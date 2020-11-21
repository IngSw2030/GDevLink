from usuarios.models import Usuario
from comunicacion.IManejadorComunicacion import IManejadorComunicacion
from comunicacion.models import Conversacion, Mensaje

#Clase que implementa la interfaz IManejadorComunicacion
class ManejadorComunicacion(IManejadorComunicacion):
    def obtenerConversaciones(nombreUsuario):
        #Cambiar por el método obtenerUsuario cuando se refactorice la app Usuarios
        usuario = Usuario.objects.get(username=nombreUsuario)
        #Si no se pudo encontrar un usuario con el nombre de usuario especificado,
        #se retorna None
        if usuario is None:
            return None
        #Si el usuario fue encontrdo, se retornan sus conversaciones.
        else:
            return usuario.conversaciones.all()

    def obtenerMensajes(nombreUsuario, idConversacion):
        #Cambiar por el método obtenerUsuario cuando se refactorice la app Usuarios
        usuario = Usuario.objects.get(username=nombreUsuario)
        #Se obtiene la conversación asociada al id solicitado
        conversacion = Conversacion.objects.get(id=idConversacion)
        #Si la conversación o el usuario especificados no existen, se retorna None
        if usuario is None or conversacion is None:
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
        #Cambiar por el método obtenerUsuario cuando se refactorice la app Usuarios
        usuario1 = Usuario.objects.get(username=nombreUsuario1)
        #Cambiar por el método obtenerUsuario cuando se refactorice la app Usuarios
        usuario2 = Usuario.objects.get(username=nombreUsuario2)
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