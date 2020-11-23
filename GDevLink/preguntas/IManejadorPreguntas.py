#Interfaz del manejador de preguntas
class IManejadorPreguntas:
    #Método que retorna una lista con las preguntas ordenadas
    #por popularidad, desde la mas popular a la menos popular.
    #Si no hay preguntas se retorna la lista vacia. 
    def obtenerPreguntasPopulares():
        pass

    #Método que crea una pregunta. Recibe el titulo de la pregunta,
    #el texto de la pregunta y el nombre del usuario que creo la 
    #pregunta. Si la pregunta es creada exitosamente retorna la pregunta,
    #si ocurre un error retorna none.
    def crearPregunta(tituloPregunta, textoPregunta, autor):
        pass

    #Método busca una pregunta por id. En caso de que no exista retorna none.
    def verPregunta(idPregunta):
        pass

    #Método que crea una respuesta a una pregunta. 
    #Recibe el id de la pregunta, el texto de la respuesta y el
    #nombre del usuario creador de la respuesta. Retorna 0 en caso 
    #de exito o 1 si ocurre un error inesperado
    def responderPregunta(idPregunta, texto, autor):
        pass

    #Método que permite seleccionar una respuesta como mejor respuesta.
    #Retorna 0 en caso de exito o 1 en caso de un error inesperado.
    def escogerRespuesta(idPregunta, idRespuesta):
        pass

    #Método que permite puntuar una pregunta positivamente.
    #Recibe el id de la pregunta y el nombre del usuario que
    #esta poniendo el punto. Si la pregunta ya estaba puntuada por
    #el usuario se, le quita el punto positivo.
    def puntuarPreguntaPos(idPregunta, nombreUsuaro):
        pass

    #Métodoque permite puntuar una pregunta negativamente.
    #Recibe el id de la pregunta y el nombre del usuario que
    #esta poniendo el punto. Si la pregunta ya estaba puntuada por
    #el usuario, se le quita el punto positivo.
    def puntuarPreguntaNeg(idPregunta, nombreUsuaro):
        pass

    #Método que permite puntuar una respuesta positivamente.
    #Recibe el id de la respuesta y el nombre del usuario que
    #esta poniendo el punto. Si la respuesta ya estaba puntuada por
    #el usuario se, le quita el punto positivo.
    def puntuarRespuestaPos(idRespuesta, nombreUsuaro):
        pass

    #Métodoque permite puntuar una respuesta negativamente.
    #Recibe el id de la respuesta y el nombre del usuario que
    #esta poniendo el punto. Si la respuesta ya estaba puntuada por
    #el usuario, se le quita el punto positivo.
    def puntuarRespuestaNeg(idRespuesta, nombreUsuaro):
        pass


