#Interfaz del manejador de proyectos
class IManejadorProyectos:
    #Metodo que crea un nuevo proyecto con los parametros
    #Retorna 1 si pudo ser creado el proyecto y -1 si no
    def crearProyecto(usuario, nombreProyecto, generos, fase, descripcion, frameworks, enlaceVideo, enlaceDescarga, roles, imagen):
        pass

    #Metodo que actualiza los datos de un proyecto dado por nombreProyecto, con los atributos de los parametros
    #Retorna 1 si pudo ser editado, -1 si no y None si no existe el proyecto
    def editarProyecto(nombreProyecto, generos, fase, descripcion, frameworks, enlaceVideo, enlaceDescarga, roles, imagen):
        pass

    #Metodo que agrega un usuario a un proyecto
    #Retorna 1 si pudo ser agregado, y -1 si no
    def agregarMiembro(nombreProyecto, nombreUsuario):
        pass

    #Metodo que saca a un usuario de un proyecto
    #Retorna 1 si pudo ser quitado, y -1 si no
    def quitarMiembro(nombreProyecto, nombreUsuario):
        pass

    #Metodo que promueve un usuario a administrador de un proyecto
    #Retorna 1 si pudo ser promovido, y -1 si no
    def promoverMiembro(nombreProyecto, nombreUsuario):
        pass

    #Metodo que revoca un usuario de ser administrador de un proyecto
    #Retorna 1 si pudo ser revocado, y -1 si no
    def revocarMiembro(nombreProyecto, nombreUsuario):
        pass

    #Metodo que crea una nueva actualización de un proyecto con los datos de los parametros texto e imagen
    def nuevaActualizacion(nombreProyecto, texto, imagen):
        pass

    #Metodo que crea una relación entre un usuario y un proyecto de seguimiento
    def seguirProyecto(usuario, nombreProyecto):
        pass

    #Metodo para obtener un proyecto dado su nombre
    #retorna el proyecto o la ausencia de este si no se encuentra
    def obtenerProyecto(nombreProyecto):
        pass

    #Método para obtener todos los proyectos de un usuario
    #retorna una lista de proyectos
    def obtenerProyectosUsuario(usuario):
        pass

    #Método para obtener los 50 proyectos con mas seguidores
    #retorna una lista de proyectos
    def obtenerProyectosPopulares():
        pass

    #Método para obtener las actualizaciones de los proyectos seguidos por un usuario
    #retorna una lista de actualizaciones
    def obtenerActualizacionesSeguidos(nombreUsuario):
        pass

    #Método para obtener uno o los proyectos que sean aceptados por los criterios de los parametros
    #Solo es obligatorio que alla un parametro no nulo
    #Retorna una lista de proyectos si los encontro, si no, estará vacía
    def buscarProyecto(nombre, genero, fase, framework):
        pass

    #Método para obtener los miembros de un proyecto
    #Retorna una lista de usuarios si los encontro, si no, estará vacía
    def obtenerMiembros(nombreProyecto):
        pass

    #Método para obtener las participaciones de un proyecto
    #Retorna una lista de participaciones si las encontro, si no, estará vacía
    def obtenerParticipaciones(nombreProyecto):
        pass

    #Método para obtener todos los miembros de un proyecto que sean administradores
    #Retorna una lista de usuarios    
    def obtenerAdministradores(nombreProyecto):
        pass
    
    #Método para obtener todas las actualizaciones de un proyecto
    #Retorna una lista de actualizaciones
    def obtenerActualizaciones(nombreProyecto):
        pass

    #Método para obtener todas las participaciones de un usuario
    #Retorna una lista de participaciones
    def obtenerParticipacionesUsuario(usuario):
        pass