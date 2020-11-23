#Interfaz del manejador de los usuarios
class IManejadorUsuarios:
    #Método que registra un nuevo usuario. Si el correo o el
    #nombre de usuario ya pertenecen a otra cuenta o si ocurre
    #algún otro problema en la creación del usuario, el usuario
    #no se registra y se retorna None. En caso contrario, se retorna
    #el objeto usuario creado.
    def registrar(nombreUsuario, email, roles, generos, frameworks, password):
        pass
    
    #Método que retorna el usuario con el nombre de usuario
    #especificado. En caso de que no haya ningún usuario con
    #este nombre de usuario, se retorna None.
    def obtenerUsuario(nombreUsuario):
        pass

    #Método que intenta hacer login con el usuario y la contraseña
    #especificados. En caso de que la autenticación sea exitosa,
    #se retorna el usuario. En caso contrario, se retorna None.
    def login(request, nombreUsuario, password):
        pass
    
    #Método que hace logout
    def logOut(request):
        pass
    
    #Método que cambia los atributos del usuario cuyo nombre de usuario
    #es recibido como parámetro, de acuerdo a los valores recibidos como
    #parámetros. Si la edición es exitosa, se retorna el usuario, en caso
    #contrario se retorna None.
    def editarPerfil(nombreUsuario, roles, generos, frameworks, descripcion, imagen):
        pass

    #Método que cambia la contrasena de un usuario a partir de la información
    #de una solicitud. Si la solicitud es válida, se hace el cambio y se retorna
    #True, en caso contrario se retorna False.
    def cambiarContrasena(request):
        pass