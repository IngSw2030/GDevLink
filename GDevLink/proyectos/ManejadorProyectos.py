from proyectos.models import Proyecto, Participacion, Actualizacion
from usuarios.models import Usuario
from proyectos.IManejadorProyectos import IManejadorProyectos
from usuarios.ManejadorUsuarios import ManejadorUsuarios
from main.enum import PosiblesFrameworks, PosiblesGeneros, PosiblesRoles, PosiblesPermisos, PosiblesFases
from django.db import IntegrityError


#clase que implementa IManjeadorProyectos
class ManejadorProyectos(IManejadorProyectos):
    
    def crearProyecto(usuario, nombreProyecto, generos, fase, descripcion, frameworks, enlaceVideo, enlaceDescarga, roles, imagen):
        
        #Se verifica si ya existe un proyecto con el nombre
        existente = Proyecto.objects.filter(nombre=nombreProyecto).count()
        #Si ya existe el proyecto, se retorna None
        if existente.count() > 0:
            return existente.all()[0]
        try:
            #Se crea el proyecto con los atributos pasados por parametro
            proyecto = Proyecto(nombre=nombreProyecto,generos=generos,fase=fase,descripcion=descripcion,frameworks=frameworks,enlace_video=enlace_video,enlace_juego=enlace_juego,imagen=imagen)
            proyecto.save()
        except IntegrityError as e:
            print(e)
            return -1
        #Luego se crea la relación de participación maestro entre el usuario creador y el proyecto
        try:
            participacion= Participacion(usuario=usuario,proyecto=proyecto,roles=roles,permiso=PosiblesPermisos.MASTER)
            participacion.save()
        except IntegrityError as e:
            return -1
        return 1

    def editarProyecto(nombreProyecto, generos, fase, descripcion, frameworks, enlaceVideo, enlaceDescarga, imagen):

        proyecto = Proyecto.objects.get(nombre=nombreProyecto)
        #Si no existe un proyecto con el nombre especificado, se retorna None
        if proyecto is None:
            return None
        #Se reemplazan los campos del proyecto por los nuevos datos establecidos
        try:
            proyecto.generos = generos
            proyecto.fase = fase
            proyecto.descripcion = descripcion
            proyecto.frameworks = frameworks
            proyecto.enlace_video = enlaceVideo
            proyecto.enlace_juego = enlaceDescarga
            proyecto.imagen = imagen
            #Se guarda el proyecto en la base de datos
            proyecto.save()
        except IntegrityError as e:
            return -1
        
    def agregarMiembro(nombreProyecto, nombreUsuario, roles):
        
        try:
            proyecto = ManejadorProyectos.obtenerProyecto(nombreProyecto)
            print(proyecto)
            usuario = ManejadorUsuarios.obtenerUsuario(nombreUsuario)
            print(nombreUsuario)
            #Si el proyecto no existe se retorna None
            if proyecto is None:
                return None
            #Se crea una relación de participación con permisos de miembro al usuario obtenido
            #con el proyecto obtenido
            participacion = Participacion(usuario=usuario,proyecto=proyecto,roles=roles,permiso=PosiblesPermisos.MIEMBRO)
            participacion.save()
            return 1
        except IntegrityError as e:
            return -1

    def quitarMiembro(nombreProyecto, nombreUsuario):
        try:
            #Se obtiene el usuario
            usuario = ManejadorUsuarios.obtenerUsuario(nombreUsuario)
            #Se obtiene el proyeto
            proyecto = ManejadorProyectos.obtenerProyecto(nombreProyecto)
            #Se obtiene la parcicipación entre el usuario y el proyecto
            participacion = Participacion.objects.get(usuario = usuario)
            #Se elimina la participacion
            participacion.delete()
            return 1
        except IntegrityError as e:
            return -1

    def promoverMiembro(nombreProyecto, nombreUsuario):
        try:
            #Se obtiene el objeto proyecto y el objeto usuario al que se promovera
            usuario = ManejadorUsuarios.obtenerUsuario(nombreUsuario)
            proyecto = ManejadorProyectos.obtenerProyecto(nombreProyecto)
            participacion = Participacion.objects.get(usuario=usuario)
            #Se cambia los permisos de la participación del usuario a administrador
            participacion.permiso = PosiblesPermisos.ADMIN
            participacion.save()
            return 1
        except IntegrityError as e:
            return -1    

    def revocarMiembro(nombreProyecto, nombreUsuario):
        try:
            usuario = ManejadorUsuarios.obtenerUsuario(nombreUsuario)
            proyecto = Proyecto.objects.get(nombre=nombreProyecto)
            participacion = Participacion.objects.get(usuario=usuario)
            #Se establece que la participación entre un proyecto y un usuario sera solo
            #con permisos de miembro
            participacion.permiso = PosiblesPermisos.MIEMBRO
            participacion.save()
            return 1
        except IntegrityError as e:
            return -1  

    def nuevaActualizacion(nombreProyecto, texto, imagen):
        proyecto = ManejadorProyectos.obtenerProyecto(nombreProyecto)
        try:
            #Se cree y guarda la nueva actualización del proyecto
            actualizacion = Actualizacion(proyecto=proyecto,descripcion=texto,imagen=imagen)
            actualizacion.save()
            return 1
        except IntegrityError as e:
            return -1

    def seguirProyecto(usuario, nombreProyecto):
        proyecto = ManejadorProyectos.obtenerProyecto(nombreProyecto)
        
        #Si el usuario ya sigue al proyecto, entonces lo deja de seguir
        if usuario in proyecto.seguidores.all():
            proyecto.seguidores.remove(usuario)
        else:
            #Si no lo sigue, entonces lo empieza a seguir
            proyecto.seguidores.add(usuario)
        #Se actualizan los seguidores del proyecto
        proyecto.save()

    def obtenerProyecto(nombreProyecto):
        
        try:
            #Se obtiene el proyecto que tenga el mismo nombre del parametro
            proyecto = Proyecto.objects.get(nombre=nombreProyecto)
        except Proyecto.DoesNotExist:
            return -1
        return proyecto

    def obtenerProyectosUsuario(usuario):
        proyectos = []
       
        #Se verifica si el usuario participa en un proyecto
        if usuario.participaciones:   
           #Se recorren todas las participaciones de un usuario
           for participacion in usuario.participaciones.all():
               #Por cada participación, se añade el proyecto a la lista de proyectos
               proyectos.append(participacion.proyecto)
        return proyectos

    def obtenerProyectosPopulares():
        #Se obtienen los 20 proyectos mas populares, ordenados por seguidores
        populares = Proyecto.objects.all().order_by('seguidores')[:10]
        return populares

    def obtenerActualizacionesSeguidos(nombreUsuario):
        usuario = Usuario.objects.get(username=nombreUsuario)
        try:
               #Se obtienen las actualizaciones de los proyectos seguidos por el usuario, ordenadas descendentemente por fecha
               actualizaciones = Actualizacion.objects.order_by("-fecha").filter(proyecto__in = usuario.proyectos_seguidos.all())
               #Se dividen los resultados en páginas de 5 actualizaciones
               paginas = Paginator(actualizaciones, 5)
               #Si el número de página solicitada no se encuentra en el rango, se utiliza la primera página
               if numero_pagina not in paginas.page_range:
                    numero_pagina = 1
               #Se obtiene la página
               pagina = paginas.page(numero_pagina)
               #Se revisa si hay página anterior
               if pagina.has_previous():
                    pagina_anterior = numero_pagina - 1
               #Se revisa si hay página siguiente
               if pagina.has_next():
                    pagina_siguiente = numero_pagina + 1
               rolesUser = request.user.roles
               vacantes = []
               #fase = PosiblesFases.labels[PosiblesFases.values.index(proyecto.fase)]
               for r in rolesUser:
                    vacantes = vacantes + list(PosicionVacante.objects.filter(roles__contains=[r])) 
        except Actualizacion.DoesNotExist:
               actualizaciones = []

    def buscarProyecto(nombre, genero, fase, framework):
        #Si la busqueda es solo por nombre, se retorna los proyecots
        #que en su nombre contengan el string dado en el parametro nombre
        if nombre != "":
            return Proyecto.objects.filter(nombre__contains = nombre)
        proyectos = []
        #Si se especificaron generos, se procede a filtrar por genero
        if len(genero) > 0:
            #De la base de datos se obtienen todos los proyectos que contengan el o los generos especificados
            proyectos = Proyecto.objects.filter(fase__contains = [genero] )
        #Si se especifico una fase, se procede a filtrar por fase
        if len(fase) > 0:
            #Con los proyectos actuales se filtran los que esten en una fase especificada
            proyectos = proyectos.filter(fase = fase)
        #Si se especificaron frameworks, se procede a filtrar por framework
        if len(framework) > 0:
            #Con los proyectos actuales se filtran los que usen un framework especificado
            proyectos = proyectos.filter(frameworks__contains = [framework]) 

        return proyectos

    def obtenerMiembros(nombreProyecto):
            proyecto = ManejadorProyectos.obtenerProyecto(nombreProyecto)
            personas = []
            #Se obtienen todos los usuarios que participan en un proyecto
            for auxPersonas in proyecto.participaciones.all():
                personas.append(auxPersonas.usuario)
            return personas

    def obtenerParticipaciones(nombreProyecto):
        proyecto = ManejadorProyectos.obtenerProyecto(nombreProyecto)
        #Se retorna todas las participaciones de un proyecto
        return proyecto.participaciones.all()

    def obtenerAdministradores(nombreProyecto):
       proyecto = ManejadorProyectos.obtenerProyecto(nombreProyecto)
       personas = []
       #Se obtienen todos los usuarios que administran un proyecto
       for auxPersonas in proyecto.participaciones.all():
            if auxPersonas.permiso ==  PosiblesPermisos.ADMIN or auxPersonas.permiso ==  PosiblesPermisos.MASTER:
                    personas.append(auxPersonas.usuario)
       return personas

    def obtenerActualizaciones(nombreProyecto):
        proyecto = ManejadorProyectos.obtenerProyecto(nombreProyecto)
        actualizaciones = []
        try:
            #Se obtiene el proyecto que tenga el mismo nombre del parametro
            actualizaciones = proyecto.actualizaciones.all()
        except Actualizacion.DoesNotExist:
            return -1
        return actualizaciones