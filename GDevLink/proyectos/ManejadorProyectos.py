from proyectos.models import Proyecto, Participacion, Actualizacion
from usuarios.models import Usuario


#clase que implementa IManjeadorProyectos
class ManejadorProyectos(IManjeadorProyectos):
    
    def crearProyecto(usuario, nombreProyecto, generos, fase, descripcion, frameworks, enlaceVideo, enlaceDescarga, roles, imagen):
        
        #Se verifica si ya existe un proyecto con el nombre
        existente = Proyecto.objects.filter(nombre=nombre).count()
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

    def editarProyecto(nombreProyecto, generos, fase, descripcion, frameworks, enlaceVideo, enlaceDescarga, roles, imagen):

        proyecto = Proyecto.objects.get(nombre=nombre)
        #Si no existe un proyecto con el nombre especificado, se retorna None
        if proyecto is None:
            return None
        #Se reemplazan los campos del proyecto por los nuevos datos establecidos
        try:
            proyecto.generos = generos
            proyecto.fase = fase
            proyecto.descripcion = descripcion
            proyecto.frameworks = frameworks
            proyecto.enlace_video = enlace_video
            proyecto.enlace_juego = enlace_descargar
            proyecto.imagen = imagen
            #Se guarda el proyecto en la base de datos
            proyecto.save()
         except IntegrityError as e:
            return -1
        
    def agregarMiembro(nombreProyecto, nombreUsuario, roles):
        
        try:
            proyecto = obtenerProyecto(nombreProyecto)
            usuario = Usuario.objects.get(username=nombreUsuario) 
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
        try
        #Se obtiene el usuario
        usuario = Usuario.objects.get(username=nombreUsuario) 
        #Se obtiene el proyeto
        proyecto = obtenerProyecto(nombre=nombre)
        #Se obtiene la parcicipación entre el usuario y el proyecto
        participacion = Participacion.objects.get(usuario = usuario)
        #Se elimina la participacion
        participacion.delete()
            return 1
        except IntegrityError as e:
            return -1

    def promoverMiembro(nombreProyecto, nombreUsuario):
        try
            #Se obtiene el objeto proyecto y el objeto usuario al que se promovera
            usuario = Usuario.objects.get(username=nombreUsuario)
            proyecto = obtenerProyecto(nombreProyecto)
            participacion = Participacion.objects.get(usuario=usuario)
            #Se cambia los permisos de la participación del usuario a administrador
            participacion.permiso = PosiblesPermisos.ADMIN
            participacion.save()
            return 1
        except IntegrityError as e:
            return -1    

    def revocarMiembro(nombreProyecto, nombreUsuario):
        try
            usuario = Usuario.objects.get(username=nombreUsuario) 
            proyecto = Proyecto.objects.get(nombre=nombreProyecto)
            participacion = Participacion.objects.get(usuario=nuevo_usuario)
            #Se establece que la participación entre un proyecto y un usuario sera solo
            #con permisos de miembro
            participacion.permiso = PosiblesPermisos.MIEMBRO
            participacion.save()
            return 1
        except IntegrityError as e:
            return -1  

    def nuevaActualizacion(nombreProyecto, texto, imagen):
        proyecto = obtenerProyecto(nombreProyecto)
        try:
            #Se cree y guarda la nueva actualización del proyecto
            actualizacion = Actualizacion(proyecto=proyecto,descripcion=texto,imagen=imagen)
            actualizacion.save()
            return 1
        except IntegrityError as e:
            return -1

    def seguirProyecto(usuario, nombreProyecto):
        proyecto = ManejadorProyectos.obtenerProyecto(nombreProyecto)
        usuario = Usuario.objects.get(username=request.user.get_username())
        #Si el usuario ya sigue al proyecto, entonces lo deja de seguir
        if usuario in proyecto.seguidores.all():
            proyecto.seguidores.remove(usuario)
        else:
            #Si no lo sigue, entonces lo empieza a seguir
            proyecto.seguidores.add(usuario)
        #Se actualizan los seguidores del proyecto
        proyecto.save()

    def obtenerProyecto(nombreProyecto):
        return Proyecto.objects.get(nombre=nombreProyecto)

    def obtenerProyectosUsuario(usuario):
        if request.user.participaciones:
           proyectos = []
           for participacion in usuario.participaciones.all():
               proyectos.append(participacion.proyecto)
        return proyectos

    def obtenerProyectosPopulares():
        todos = Proyecto.objects.all().order_by('seguidores')
        populares = [None] * 4
        i=0
        for pop in todos:
            populares[i] = pop
              if i == 10:
                   break
            i = i+1
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
        pass

    def obtenerMiembros(nombreProyecto):
            proyecto = ManejadorProyectos.obtenerProyecto(nombre=nombre)
            personas = []
                for auxPersonas in proyecto.participaciones.all():
                    personas.append(auxPersonas.usuario)
            return personas

    def obtenerParticipaciones(nombreProyecto):
        proyecto = ManejadorProyectos.obtenerProyecto(nombre=nombre)
        return proyecto.participaciones.all()