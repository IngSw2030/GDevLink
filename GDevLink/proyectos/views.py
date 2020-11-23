from django.shortcuts import render

from main.enum import PosiblesFrameworks, PosiblesGeneros, PosiblesRoles, PosiblesPermisos, PosiblesFases
from proyectos.models import Proyecto, Participacion, Usuario, Actualizacion
from datetime import datetime
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.urls import reverse
from django.http import HttpResponse, HttpResponseRedirect
from proyectos.ManejadorProyectos import ManejadorProyectos
# Create your views here.

    
@login_required
def crearProyecto(request):
    if request.method == "POST" and 'crearProyecto' in request.POST:
        #Se obtienen los datos de los campos del formulario de creación de proyectos
        nombre = request.POST["name"]
        generos = request.POST.getlist("generos")
        fase = request.POST.getlist('fase')
        descripcion = request.POST['descripcion']
        frameworks = request.POST.getlist('frameworks')
        enlace_video =request.POST["enlaceVideo"]
        enlace_juego = request.POST["enlacedescargar"]
        roles = request.POST.getlist("roles")

        #Se verifica que se hallan rellenado los campos obligatorios
        if(nombre == ""):
            return render(request,"proyectos/crearProyecto.html",{"generos":PosiblesGeneros ,"fases":PosiblesFases ,"frameworks":PosiblesFrameworks,"roles":PosiblesRoles,
             "message": "Por favor ingresar un nombre"})
        if(len(fase)!=1):
            return render(request,"proyectos/crearProyecto.html",{"generos":PosiblesGeneros ,"fases":PosiblesFases ,"frameworks":PosiblesFrameworks,"roles":PosiblesRoles,
             "message": "Seleccione una (1) fase"})
        if(len(frameworks)==0):
            return render(request,"proyectos/crearProyecto.html",{"generos":PosiblesGeneros ,"fases":PosiblesFases ,"frameworks":PosiblesFrameworks,"roles":PosiblesRoles,
             "message": "Seleccione al menos un (1) framework"})
        fase = fase[0]
        if 'imagen' in request.FILES:
            imagen = request.FILES['imagen']
        else:
            imagen=None

        result = ManejadorProyectos.crearProyecto(request.user, nombre, generos, fase, descripcion, frameworks, enlace_video, enlace_juego, roles, imagen)
        
        if result is None:
            return render(request,"proyectos/crearProyecto.html",{"generos":PosiblesGeneros ,"fases":PosiblesFases ,"frameworks":PosiblesFrameworks,"roles":PosiblesRoles,
             "message": "Nombre de proyecto ya registrado"})

        if result = -1:
            return render(request,"proyectos/crearProyecto.html",{"generos":PosiblesGeneros ,"fases":PosiblesFases ,"frameworks":PosiblesFrameworks,"roles":PosiblesRoles,
             "message": "Error al crear el proyecto"})
        
        return HttpResponseRedirect(reverse("proyecto", kwargs={"nombre": nombre}))
                
    return render(request,"proyectos/crearProyecto.html",{"generos":PosiblesGeneros ,"fases":PosiblesFases ,"frameworks":PosiblesFrameworks,"roles":PosiblesRoles})

def proyecto(request,nombre):
    try:
        proyecto = Proyecto.objects.get(nombre=nombre)
        generos = []
        frameworks = []
        participaciones = {}
        actualizaciones = {}
        fase = PosiblesFases.labels[PosiblesFases.values.index(proyecto.fase)]
        for genero in proyecto.generos:
            generos.append((PosiblesGeneros.labels[PosiblesGeneros.values.index(genero)]))
        for framework in proyecto.frameworks:
            frameworks.append((PosiblesFrameworks.labels[PosiblesFrameworks.values.index(framework)]))
        for participacion in proyecto.participaciones.all():
            roles_p = ""
            for rol in participacion.roles:
                roles_p= roles_p + " " + str(PosiblesRoles.labels[PosiblesRoles.values.index(rol)])
            roles_p = roles_p + " - " + str(PosiblesPermisos.labels[PosiblesPermisos.values.index(participacion.permiso)])
            participaciones[participacion.usuario.username] = roles_p
        actualizaciones = proyecto.actualizaciones.all()
        for act in actualizaciones:
            print(act.descripcion)

        participacion = Participacion.objects.get(usuario=request.user, proyecto=proyecto)
        if participacion.permiso == PosiblesPermisos.MASTER or participacion.permiso == PosiblesPermisos.ADMIN:
            admin = True
        else:
            admin = False
        #Revisar si el usuario sigue el proyecto
        usuario = Usuario.objects.get(username=request.user.get_username())
        if usuario.proyectos_seguidos.filter(nombre = nombre):
            siguiendo = True
        else:
            siguiendo = False
        return render(request, "proyectos/proyecto.html", {
            "proyecto": proyecto,
            "generos": generos,
            "miembros": participaciones,
            "frameworks": frameworks,
            "fase": fase,
            "actualizaciones": actualizaciones,
            "seguidores": proyecto.numero_seguidores(),
            "siguiendo": siguiendo,
            "administrador":admin
        })
    except Proyecto.DoesNotExist:
        return render(request, "main/error.html", {
            "mensaje": "Proyecto no encontrado."
        })

def proyectosUsuario(request):
    if request.user.is_authenticated:
        proyectos = ManejadorProyectos.obtenerProyectosUsuario(request.user)
           return render(request,"proyectos/proyectosUsuario.html",{"proyectos": proyectos})    
    return render(request,"proyectos/proyectosUsuario.html")
       #else
    #else

def editarProyecto(request, nombre):
    if request.method == "POST" and 'Actualizar' in request.POST: 
        #Se obtienen los datos de los campos del formulario de edición de proyectos
        generos = request.POST.getlist("generos")
        fase = request.POST.getlist('fase')
        descripcion = request.POST['descripcion']
        frameworks = request.POST.getlist('frameworks')
        enlace_video =request.POST["enlaceVideo"]
        enlace_descargar = request.POST["enlaceDescargar"]
        
        #Se verifica que se hallan rellenado los campos obligatorios
        if(len(fase)!=1):
            return render(request, "main/error.html", {
                "mensaje": " Debe seleccionar (1) fase."
            })
        if(len(frameworks)==0):
            return render(request, "main/error.html", {
                "mensaje": "Debe seleccionar al menos (1) framework."
            })
        if(len(generos)==0):
            return render(request, "main/error.html", {
                "mensaje": "Debe seleccionar al menos (1) genero."
            })
        fase = fase[0]

        user = Usuario.objects.get(username=request.user)

        if 'imagen' in request.FILES:
            imagen = request.FILES['imagen']
        else:
            imagen=user.imagen

        #Se llama al controlador de proyecto para que lo edite
        result = ManejadorProyectos.editarProyecto(nombre, generos, fase, descripcion, frameworks, enlace_video, enlace_juego, roles, imagen)
        
         
        #Si result es -1, el proyecto no pudo ser editado correctamente
        if result = -1:
            return render(request, "main/error.html", {
                "mensaje": "Proyecto no encontrado."
            })
        return HttpResponseRedirect(reverse("proyecto",kwargs={"nombre": nombre}))
    else:
        try:
            proyecto = Proyecto.objects.get(nombre=nombre)
            generos = []
            frameworks = []
            participaciones = {}
            fase = PosiblesFases.labels[PosiblesFases.values.index(proyecto.fase)]
            for genero in proyecto.generos:
                generos.append((PosiblesGeneros.labels[PosiblesGeneros.values.index(genero)]))
            for framework in proyecto.frameworks:
                frameworks.append((PosiblesFrameworks.labels[PosiblesFrameworks.values.index(framework)]))
            for participacion in proyecto.participaciones.all():
                roles_p = ""
                for rol in participacion.roles:
                    roles_p= roles_p + " " + str(PosiblesRoles.labels[PosiblesRoles.values.index(rol)])
                participaciones[participacion.usuario.username] = roles_p
                #Se renderiza la página de edición de proyecto, con sus atributos
            return render(request, "proyectos/editarProyecto.html", {
                        "proyecto": proyecto,
                        "generos": generos,
                        "miembros": participaciones,
                        "frameworks": frameworks,
                        "fase": fase,
                        "posiblesgeneros": PosiblesGeneros,
                        "posiblesfases": PosiblesFases,
                        "posiblesframeworks" : PosiblesFrameworks,
                        "posiblesroles": PosiblesRoles
            })
        except Proyecto.DoesNotExist:
            return render(request, "main/error.html", {
                "mensaje": "Proyecto no encontrado."
            })
            
def gestionMiembros (request, nombre):
    proyecto = ManejadorProyectos.obtenerProyecto(nombre)
    #Se obtienen las participaciones del proyecto
    participacionesPro = ManejadorProyectos.obtenerParticipaciones(nombre)
    participaciones = {}
    #Se crea una lista de participaciones, en donde cada elemento es un string con 
    #el nombre del usuario, seguido de sus roles en el proyecto
    for participacion in participacionesPro:
                roles_p = ""
                for rol in participacion.roles:
                    roles_p= roles_p + " " + str(PosiblesRoles.labels[PosiblesRoles.values.index(rol)]) 
                    
                roles_p = roles_p + " - " + str(PosiblesPermisos.labels[PosiblesPermisos.values.index(participacion.permiso)])
                participaciones[participacion.usuario.username] = roles_p

    return render(request,"proyectos/gestionMiembros.html",{
        "proyecto": proyecto,
        "miembros": participaciones
    } )

def agregarMiembros (request, nombre):
    if request.method == "POST" and 'Agregar' in request.POST: 
        roles = request.POST.getlist("roles")
        nom_us = request.POST["nuevoMiembro"]
        #Se llama al manejador para que agrege el miembro al proyecto
        result = ManejadorProyectos.agregarMiembro(nombre,)
        #Si result es none, el proyecto no existe
        if result = None:
            return render(request, "main/error.html", {
            "mensaje": "El proyecto no existe."
        })
        #Si result es -1, hubo un error inesperado
        if result = -1
            return render(request, "main/error.html", {
                "mensaje": "Se produjo un error en agregar nuevo miembro"
            })
        #Se retorna la página de gestión con los datos actualizados
        return HttpResponseRedirect(reverse("gestionMiembros", kwargs={"nombre": nombre})) 
    else:
        try:
            #Si el request no es POST, entonces se renderiza la página
        
            proyecto = ManejadorProyectos.obtenerProyecto(nombre=nombre)
            #Se obtiene una lista de todos los usuarios como JSON
            #result_list = list(Usuario.objects.all().values('username'))
            #dataJSON = dumps(result_list) 
            usuarios = Usuario.objects.all()

            #Se renderiza la página de agregar miembros
            personas = ManejadorProyectos.obtenerMiembros(nombre)
            return render(request,"proyectos/agregarMiembros.html",{
                "miembros": personas,
                "proyecto": proyecto,
                "users": usuarios,
                "posiblesroles": PosiblesRoles
                
            })
        except Proyecto.DoesNotExist:
            return render(request, "main/error.html", {
                "mensaje": "Proyecto no encontrado."
            })




def eliminarMiembros (request, nombre):
    if request.method == "POST" and 'Eliminar' in request.POST: 
        nom_us = request.POST["eliminarMiembro"]
        
            #Se llama al manejador para que elimine al miembro del proyecto
            result = ManejadorProyectos.quitarMiembro(nombre,nom_us)
            #Si result es -1 hubo un error inesperado
            if result = -1
                return render(request, "main/error.html", {
                "mensaje": "El Usuario no participa en el proyecto."
            })
            #Se carga la página de gestión con el usuario ya eliminado
            return HttpResponseRedirect(reverse("gestionMiembros", kwargs={"nombre": nombre})) 
        
    else:
        try:
            participacionesTodas = ManejadorProyectos.obtenerParticipaciones(nombre)
            personas = []
            for auxPersonas in proyecto.participaciones.all():
                if auxPersonas.permiso !=  PosiblesPermisos.MASTER:
                    personas.append(auxPersonas.usuario)      
            usuarios = Usuario.objects.all()
            #Se renderiza la página de eliminar miembros   
            proyecto = ManejadorProyectos.obtenerProyecto(nombre=nombre)
            
             usuarios = Usuario.objects.all()
            return render(request,"proyectos/eliminarMiembros.html",{
                "miembros": personas,
                "proyecto": proyecto,
                "usuarios": usuarios           
            } )
        except Proyecto.DoesNotExist:
            return render(request, "main/error.html", {
                "mensaje": "Error inesperado."
            })

def agregarAdministrador (request, nombre):
    if request.method == "POST" and 'Agregar' in request.POST: 

        nom_us = request.POST["nuevoAdmin"]
        #Se llama al manejador para que promueva un miembro de un proyecto a administrador       
        result = ManejadorProyectos.promoverMiembro(nombre, nom_us)
        
        if result = -1:
            return render(request, "main/error.html", {
                "mensaje": "Se produjo un error al agregar un administrador"})
         return HttpResponseRedirect(reverse("gestionMiembros", kwargs={"nombre": nombre})) 
    else:
        try:
            proyecto = ManejadorProyectos.obtenerProyecto(nombre)
            personas = []
            #La lista de miembros solo es rellenada con miembros que no sean ya administradores
            for auxPersonas in proyecto.participaciones.all():
                if auxPersonas.permiso !=  PosiblesPermisos.MASTER and auxPersonas.permiso !=  PosiblesPermisos.ADMIN:
                    personas.append(auxPersonas.usuario)
             usuarios = Usuario.objects.all()
            
            #Se renderiza la página de agregar administrador
            return render(request,"proyectos/agregarAdministrador.html",{
                "miembros": personas,
                "proyecto": proyecto,
                "posiblesroles": PosiblesRoles,
                "usuarios": usuarios
            } )
        except Proyecto.DoesNotExist:
            return render(request, "main/error.html", {
                "mensaje": "Proyecto no encontrado."
            })       

def eliminarAdministrador (request, nombre):
    if request.method == "POST" and 'Eliminar' in request.POST: 
        nom_us = request.POST["eliminarAdmin"]
        #Se llama al manejador de proyectos para que revoque los permisos de administrador de un miembro
        result = ManejadorProyectos.revocarMiembro(nombre, nom_us)
        if result = -1
            return render(request, "main/error.html", {
                "mensaje": "El Usuario no participa en el proyecto."
            })
        return HttpResponseRedirect(reverse("gestionMiembros", kwargs={"nombre": nombre})) 
        
    else:
        try:
            #Se renderiza la página de remover administrador con los miembros que son administradores
            proyecto = ManejadorProyectos.obtenerProyecto(nombre)
            personas = []
            for auxPersonas in proyecto.participaciones.all():
                if auxPersonas.permiso ==  PosiblesPermisos.ADMIN:
                    personas.append(auxPersonas.usuario)
            usuarios = Usuario.objects.all()
            return render(request,"proyectos/eliminarAdministrador.html",{
                "miembros": personas,
                "proyecto": proyecto,
                "usuarios": usuarios,
                "posiblesroles": PosiblesRoles
                
            } )
        except Proyecto.DoesNotExist:
            return render(request, "main/error.html", {
                "mensaje": "Proyecto no encontrado."
            })


def nuevaActualizacion(request,nombre):
    if request.method == "POST":
        proyecto = Proyecto.objects.get(nombre=nombre)
        if 'imagenNueva' in request.FILES:
            imagen = request.FILES['imagenNueva']
        else:
            imagen=None
        descripcion = request.POST['descripcionActualizacion']
        #Se llama al manejador para que cree una nueva actualización para un proyecto
        result = ManejadorProyectos.nuevaActualizacion(nombre,descripcion,imagen)

        if result = -1:
            return HttpResponseRedirect(reverse("proyecto",kwargs={"nombre": nombre}))

    return HttpResponseRedirect(reverse("proyecto",kwargs={"nombre": nombre}))

def seguir(request,nombre):
    if request.method == 'PUT':
        ManejadorProyectos.seguirProyecto(request.user, nombre)    
    return HttpResponse(status=200)

def explorarProyectos(request):

    if request.method == "POST":
        return render(request,"proyectos/explorarProyectos.html",{
                "generos":PosiblesGeneros,
                "fases":PosiblesFases,
                "frameworks":PosiblesFrameworks
            } )

    else:
        proyectos = []
        proyectos = Proyecto.objects.all()
        todos = Proyecto.objects.all().order_by('seguidores')
        populares = [None] * 4
        i=0
        for pop in todos:
            populares[i] = pop
            if i == 3:
                break
            i = i+1

        return render(request,"proyectos/explorarProyectos.html",{
                "generos":PosiblesGeneros,
                "fases":PosiblesFases,
                "frameworks":PosiblesFrameworks,
                "proyectos":proyectos,
                "populares": populares
            } )