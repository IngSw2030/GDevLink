from usuarios.models import Usuario
from usuarios.IManejadorUsuarios import IManejadorUsuarios
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError

#Clase que implementa la interfaz IManejadorUsuarios
class ManejadorUsuarios(IManejadorUsuarios):
    def registrar(nombreUsuario, email, roles, generos, frameworks, password):
        #Si nombre de usuario, email o contraseña están vacíos, se retorna None
        if nombreUsuario == '' or email == '' or password == '':
            return None
        user = None
        #Se intenta crear el nuevo usuario
        try:
            user = Usuario.objects.create_user(nombreUsuario, email, password)
            user.roles = roles
            user.generos = generos
            user.frameworks = frameworks
            user.imagen = '/usuarios/defaultUser.png'
            user.save()
        #Si ocurre algún error en la creación del usuario, se retorna None
        except IntegrityError as e:
            return None
        return user
    
    def obtenerUsuario(nombreUsuario):
        #Se intenta obtener el usuario con el nombre de usuario recibido como parámetro
        try:
            usuario = Usuario.objects.get(username=nombreUsuario)
            return usuario
        #Se retorna None si el usuario no existe
        except Usuario.DoesNotExist:
            return None

    def login(request, nombreUsuario, password):
        #Se autentica al usuario
        user = authenticate(request, username=nombreUsuario, password=password)
        #Si la autenticación es exitosa, se hace login
        if user is not None:
            login(request, user)
        return user
    
    def logOut(request):
        logout(request)

    def editarPerfil(nombreUsuario, roles, generos, frameworks, descripcion, imagen):
        #Se intenta actualizar los datos del usuario
        try:
            #Se obtiene el usuario con el nombre de usuario recibido como parámetro
            user = Usuario.objects.get(username=nombreUsuario)
            user.roles = roles
            user.generos = generos
            user.frameworks = frameworks
            user.descripcion = descripcion
            user.imagen = imagen
            user.save()
            return user
        #Se retorna None si el usuario no existe o si ocurre algun error en la actualización de los datos
        except (IntegrityError, Usuario.DoesNotExist) as e:
            return None