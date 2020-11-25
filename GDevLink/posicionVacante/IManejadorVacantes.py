#Interfaz del manejador de las vacantes
class IManejadorVacantes:
    #Método que retorna la vacante correspondiente al id recibido
    #como parámetro o None en caso de que no exista.
    def obtenerVacante(idVacante):
        pass
    
    #Crea una nueva posición vacante asociada al proyecto cuyo nombre
    #recibe como parámetro, utilizando los demás valores recibidos.
    #En caso de que la creación sea exitosa, retorna la vacante creada
    #y en caso contrario retorna None.
    def crearVacante(nombreProyecto, roles, frameworks, descripcion):
        pass
    
    #Edita los campos de una posición vacante. Retorna la vacante
    #si la edición fue exitosa y None en caso contrario.
    def editarVacante(idVacante, roles, frameworks, descripcion):
        pass

    #Elimina la vacante cuyo nombre fue recibido como parámetro.
    #Retorna 0 si la operación fue exitosa y -1 si
    #ocurrió algún error.
    def eliminarVacante(idVacante):
        pass

    #Realiza una búsqueda de vacantes, retornando las vacantes
    #que cumplen con los criterios de búsqueda.
    def buscarVacantes(nombreProyecto, roles, frameworks):
        pass
    
    #Crea la aplicación del usuario cuyo nombre de usuario es pasado
    #como parámetro en la vacante cuyo id es pasado como parámetro.
    def aplicarVacante(nombreUsuario, idVacante):
        pass
    
    #Retorna las vacantes de un proyecto y None si ocurrió un error.
    def obtenerVacantesProyecto(nombreProyecto):
        pass
    
    #Retorna los aplicantes de la vacante cuyo id es pasado como
    #parámetro. Retorna None en caso de que ocurra algún error.
    def obtenerAplicantes(idVacante):
        pass

    #Retorna las posiciones vacantes sugeridas para el usuario
    #cuyo nombre es pasado como parámetro.
    def obtenerVacantesSugeridas(nombreUsuario):
        pass