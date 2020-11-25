from django.shortcuts import render

from main.enum import PosiblesFrameworks, PosiblesGeneros, PosiblesRoles, PosiblesPermisos, PosiblesFases
from proyectos.models import Proyecto, Participacion, Usuario, Actualizacion
from datetime import datetime
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.urls import reverse
from django.http import HttpResponse, HttpResponseRedirect
from proyectos.ManejadorProyectos import ManejadorProyectos
from usuarios.ManejadorUsuarios import  ManejadorUsuarios
from json import dumps
import json
from django.shortcuts import redirect
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
        #Se llama al manejador de proyectos para que cree un nuevo proyecto
        result = ManejadorProyectos.crearProyecto(request.user, nombre, generos, fase, descripcion, frameworks, enlace_video, enlace_juego, roles, imagen)
        
        #Si el resultado de la creacion es None, entonces ya existe un proyecto con el nombre especificado
        if result is None:
            return render(request,"proyectos/crearProyecto.html",{"generos":PosiblesGeneros ,"fases":PosiblesFases ,"frameworks":PosiblesFrameworks,"roles":PosiblesRoles,
             "message": "Nombre de proyecto ya registrado"})
        #Si el resultado es -1, hubo un error inesperado al crear el proyecto
        if result == -1:
            return render(request,"proyectos/crearProyecto.html",{"generos":PosiblesGeneros ,"fases":PosiblesFases ,"frameworks":PosiblesFrameworks,"roles":PosiblesRoles,
             "message": "Error al crear el proyecto"})
        #Si no hubieron errores, el usuario es redireccionado a la página del proyecto creado
        return HttpResponseRedirect(reverse("proyecto", kwargs={"nombre": nombre}))
    if request.method == "GET":            
        return render(request,"proyectos/crearProyecto.html",{"generos":PosiblesGeneros ,"fases":PosiblesFases ,"frameworks":PosiblesFrameworks,"roles":PosiblesRoles})

def proyecto(request,nombre):
    if request.method == "GET":
        try:
            #Se obtiene el proyecto
            proyecto = ManejadorProyectos.obtenerProyecto(nombre)
            #Se declaran variables para los datos del proyecto
            generos = []
            frameworks = []
            participaciones = {}
            actualizaciones = {}
            fase = PosiblesFases.labels[PosiblesFases.values.index(proyecto.fase)]
            #Como los generos son enumerados, la lista de generos de proyectos es rellenada con los valores
            #obtenidos por el codigo de cada genero
            for genero in proyecto.generos:
                generos.append((PosiblesGeneros.labels[PosiblesGeneros.values.index(genero)]))
            #Igual que con los generos
            for framework in proyecto.frameworks:
                frameworks.append((PosiblesFrameworks.labels[PosiblesFrameworks.values.index(framework)]))
            #Las participaciones que muestra views es una lista de strings, en el que cada uno es el nombre del usuario
            #más los roles que desempeña en el proyecto
            #Se recorren todas las participaciones del proyecto
            participacionesAll = ManejadorProyectos.obtenerParticipaciones(nombre)
            for participacion in participacionesAll:
                roles_p = ""
                #Para cada participacion se recorren sus roles
                for rol in participacion.roles:
                    #Todos los roles son concatenados
                    roles_p= roles_p + " " + str(PosiblesRoles.labels[PosiblesRoles.values.index(rol)])
                #Despues de concatenar todos los roles, se agrega el tipo de participacion del usuario
                #al final del string
                roles_p = roles_p + " - " + str(PosiblesPermisos.labels[PosiblesPermisos.values.index(participacion.permiso)])
                #String es agregado a la lista de participaciones, en la posición del usuario
                participaciones[participacion.usuario.username] = roles_p
            #Se obtienen las actualizaciones de un proyecto
            actualizaciones = ManejadorProyectos.obtenerActualizaciones(nombre)

            #Se verifica si el usuario que hace la petición es un administrador
            if request.user in ManejadorProyectos.obtenerAdministradores(nombre):
                admin = True
            else:
                admin = False
            #Revisar si el usuario sigue el proyecto
            usuario = request.user
            if usuario.proyectos_seguidos.filter(nombre = nombre):
                siguiendo = True
            else:
                siguiendo = False
            #Se envia al cliente toda la información del proyecto
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
    elif request.method == "POST" and 'Actualizar' in request.POST: 
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


        if 'imagen' in request.FILES:
            imagen = request.FILES['imagen']
        else:
            imagen=None

        if request.user in ManejadorProyectos.obtenerAdministradores(nombre):
            #Se llama al controlador de proyecto para que lo edite
            result = ManejadorProyectos.editarProyecto(nombre, generos, fase, descripcion, frameworks, enlace_video, enlace_descargar, imagen)          
         
        #Si result es -1, el proyecto no pudo ser editado correctamente
        if result == -1:
            return render(request, "main/error.html", {
                "mensaje": "Proyecto no encontrado."
            })
        return HttpResponseRedirect(reverse("proyecto",kwargs={"nombre": nombre}))

@login_required
def proyectosUsuario(request): 
    proyectos = ManejadorProyectos.obtenerProyectosUsuario(request.user)
    return render(request,"proyectos/proyectosUsuario.html",{"proyectos": proyectos})    
    
   

def editarProyecto(request, nombre):
    if request.method == "GET":
        try:
            proyecto = ManejadorProyectos.obtenerProyecto(nombre)
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
    if request.method == "GET":
        try:
            #Si el request no es POST, entonces se renderiza la página
        
            proyecto = ManejadorProyectos.obtenerProyecto(nombre)
            

            result_list = list(Usuario.objects.all().values('username'))
            miembrosNombres = list()
            usuariosNoMiembros = list()
            miembros = []
            usuarios = list(Usuario.objects.all())
           
            participacionesAll = ManejadorProyectos.obtenerParticipaciones(nombre)
            #Se rellena la lista personas con los nombres de los participantes de un proyecto
            for auxPersonas1 in participacionesAll:
                    miembrosNombres.append(auxPersonas1.usuario.username)

            #La lista usuariosNoMiembros se rellena con todos los usuarios que no sean miembros del proyecto
            for auxPersonas in result_list:
                if auxPersonas.get("username") not in miembrosNombres:
                    usuariosNoMiembros.append(auxPersonas)                

            dataJSON = dumps(usuariosNoMiembros)
            miembros = ManejadorProyectos.obtenerParticipaciones(nombre)

            #Se renderiza la página de gestion de miembros
            return render(request,"proyectos/gestionMiembros.html",{
                "miembros": miembros,
                "proyecto": proyecto,
                "usuarios": usuarios,
                "posiblesPermisos": PosiblesPermisos,
                "posiblesRoles": PosiblesRoles,
                "users": dataJSON
                
            })
        except Proyecto.DoesNotExist:
            return render(request, "main/error.html", {
                "mensaje": "Proyecto no encontrado."
            })


def miembros(request, nombre):
    if request.method == "POST": 
        roles = request.POST.getlist("roles")
        usuarioB = request.POST.getlist('usuarioB')
        proyecto = ManejadorProyectos.obtenerProyecto(nombre)    
        if(len(roles)==0):
            return render(request, "main/error.html", {
                "mensaje": "Debe seleccionar al menos (1) rol."
            })
        if(len(usuarioB)==0):
            return render(request, "main/error.html", {
                "mensaje": "Debe seleccionar un usuario."
            })
        #Se llama al manejador para que agrege el miembro al proyecto
        result = ManejadorProyectos.agregarMiembro(nombre,usuarioB[0],roles)
        #Si result es none, el proyecto no existe
        if result is None:
            return render(request, "main/error.html", {
            "mensaje": "El proyecto no existe."
        })
        #Si result es -1, hubo un error inesperado
        if result == -1:
            return render(request, "main/error.html", {
                "mensaje": "Se produjo un error en agregar nuevo miembro"
            })
        #Se retorna la página de gestión con los datos actualizados
        return HttpResponseRedirect(reverse("gestionMiembros", kwargs={"nombre": nombre})) 
    
    elif request.method == "DELETE": 
        informacion = json.loads(request.body)
        usuario = informacion.get("id")
        #Se llama al manejador para que elimine al miembro del proyecto
        result = ManejadorProyectos.quitarMiembro(nombre,usuario)
        #Si result es -1 hubo un error inesperado
        if result == -1:
            return render(request, "main/error.html", {
                "mensaje": "El Usuario no participa en el proyecto."
            })
        #Se carga la página de gestión con el usuario ya eliminado
        return HttpResponseRedirect(reverse("gestionMiembros", kwargs={"nombre": nombre}))  

def administradores (request, nombre):
    if request.method == 'POST':    
        informacion = json.loads(request.body)
        nuevo_usuario = informacion.get("id")  
        #Se llama al manejador para que promueva un miembro de un proyecto a administrador       
        result = ManejadorProyectos.promoverMiembro(nombre, nuevo_usuario)
        if result == -1:
            return render(request, "main/error.html", {
                "mensaje": "Se produjo un error al agregar un administrador"})
        return HttpResponseRedirect(reverse("gestionMiembros", kwargs={"nombre": nombre}))
    elif request.method == 'DELETE':
        informacion = json.loads(request.body)
        usuario = informacion.get("id")
        #Se llama al manejador de proyectos para que revoque los permisos de administrador de un miembro
        result = ManejadorProyectos.revocarMiembro(nombre, usuario)
        if result == -1:
            return render(request, "main/error.html", {
                "mensaje": "El Usuario no participa en el proyecto."
            })
        return HttpResponseRedirect(reverse("gestionMiembros", kwargs={"nombre": nombre}))     
   

def nuevaActualizacion(request,nombre):
    if request.method == "POST":
        if 'imagenNueva' in request.FILES:
            imagen = request.FILES['imagenNueva']
        else:
            imagen=None
        descripcion = request.POST['descripcionActualizacion']
        #Se llama al manejador para que cree una nueva actualización para un proyecto
        result = ManejadorProyectos.nuevaActualizacion(nombre,descripcion,imagen)

        if result == -1:
            return HttpResponseRedirect(reverse("proyecto",kwargs={"nombre": nombre}))

    return HttpResponseRedirect(reverse("proyecto",kwargs={"nombre": nombre}))

def seguir(request,nombre):
    if request.method == 'PUT':
        ManejadorProyectos.seguirProyecto(request.user, nombre)    
    return HttpResponse(status=200)

def explorarProyectos(request):

    if request.method == "POST":
        nombre_busqueda = request.POST['barraBusqueda']
        generos = request.POST.getlist("generos")
        fase = request.POST.getlist('fase')
        frameworks = request.POST.getlist('frameworks')

        proyectos = []

        proyectos = ManejadorProyectos.buscarProyecto(nombre_busqueda,generos,fase,frameworks)

        return render(request, "proyectos/explorarProyectos.html", {
            "generos": PosiblesGeneros,
            "fases": PosiblesFases,
            "frameworks": PosiblesFrameworks,
            "populares": proyectos
        })

    else:
        
        todos = ManejadorProyectos.obtenerProyectosPopulares()
        populares = [None] * 4
        i = 0
        for pop in todos:
            populares[i] = pop
            if i == 3:
                break
            i = i+1

        return render(request, "proyectos/explorarProyectos.html", {
            "generos": PosiblesGeneros,
            "fases": PosiblesFases,
            "frameworks": PosiblesFrameworks,
            "populares": populares
        })