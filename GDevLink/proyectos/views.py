from django.shortcuts import render
from main.enum import *
from proyectos.models import Proyecto, Participacion, Usuario, Actualizacion
from datetime import datetime
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.urls import reverse
from django.http import HttpResponse, HttpResponseRedirect
# Create your views here.

    
@login_required
def crearProyecto(request):
    if request.method == "POST" and 'crearProyecto' in request.POST:
        nombre = request.POST["name"]
        generos = request.POST.getlist("generos")
        fase = request.POST.getlist('fase')
        descripcion = request.POST['descripcion']
        frameworks = request.POST.getlist('frameworks')
        enlace_video =request.POST["enlaceVideo"]
        enlace_juego = request.POST["enlacedescargar"]
        roles = request.POST.getlist("roles")

        if(nombre == ""):
            return render(request,"proyectos/crearProyecto.html",{"generos":PosiblesGeneros ,"fases":PosiblesFases ,"frameworks":PosiblesGeneros,"roles":PosiblesRoles,
             "message": "Por favor ingresar un nombre"})
        if(len(fase)!=1):
            return render(request,"proyectos/crearProyecto.html",{"generos":PosiblesGeneros ,"fases":PosiblesFases ,"frameworks":PosiblesGeneros,"roles":PosiblesRoles,
             "message": "Seleccione una (1) fase"})
        if(len(frameworks)==0):
            return render(request,"proyectos/crearProyecto.html",{"generos":PosiblesGeneros ,"fases":PosiblesFases ,"frameworks":PosiblesGeneros,"roles":PosiblesRoles,
             "message": "Seleccione al menos un (1) framework"})
        fase = fase[0]
        if 'imagen' in request.FILES:
            imagen = request.FILES['imagen']
            galeria=[]
            galeria.append(imagen)
        else:
            imagen=None
            galeria=[]
        try:
            proyecto = Proyecto(nombre=nombre,generos=generos,fase=fase,descripcion=descripcion,frameworks=frameworks,enlace_video=enlace_video,enlace_juego=enlace_juego,imagen=imagen, galeria=galeria)
            proyecto.save()
        except IntegrityError as e:
            return render(request, "proyectos/crearProyecto.html", {
                "message": "Nombre de proyecto ya registrado"})
        try:
            participacion= Participacion(usuario=request.user,proyecto=proyecto,roles=roles,permiso=PosiblesPermisos.MASTER)
            participacion.save()
            return HttpResponseRedirect(reverse("proyecto", kwargs={"nombre": nombre}))
        except IntegrityError as e:
            return render(request, "proyectos/crearProyecto.html", {
                "message": "Error en la creacion de participacion"})
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
            participaciones[participacion.usuario.username] = roles_p
        actualizaciones = proyecto.actualizaciones.all()
        for act in actualizaciones:
            print(act.descripcion)
        return render(request, "proyectos/proyecto.html", {
            "proyecto": proyecto,
            "generos": generos,
            "miembros": participaciones,
            "frameworks": frameworks,
            "fase": fase,
            "actualizaciones": actualizaciones
        })
    except Proyecto.DoesNotExist:
        return render(request, "main/error.html", {
            "mensaje": "Proyecto no encontrado."
        })

def proyectosUsuario(request):
    
    if request.user.is_authenticated:
       
       if request.user.participaciones:
           proyectos = []
           for participacion in request.user.participaciones.all():
               proyectos.append(participacion.proyecto)
           return render(request,"proyectos/proyectosUsuario.html",{"proyectos": proyectos})
        
           
    return render(request,"proyectos/proyectosUsuario.html")
       #else
    #else

def editarProyecto(request, nombre):
    if request.method == "POST" and 'Actualizar' in request.POST: 
        generos = request.POST.getlist("generos")
        fase = request.POST.getlist('fase')
        descripcion = request.POST['descripcion']
        frameworks = request.POST.getlist('frameworks')
        enlace_video =request.POST["enlaceVideo"]
        enlace_descargar = request.POST["enlaceDescargar"]
        
        #if(len(fase)!=1):
         #   return render(request,f"proyectos/editarProyecto/{nombre}",{"generos":PosiblesGeneros ,"fases":PosiblesFases ,"frameworks":PosiblesGeneros,"roles":PosiblesRoles,
          #   "message": "Seleccione una (1) fase"})
        #if(len(frameworks)==0):
         #   return render(request,f"proyectos/editarProyecto/{nombre}",{"generos":PosiblesGeneros ,"fases":PosiblesFases ,"frameworks":PosiblesGeneros,"roles":PosiblesRoles,
          #   "message": "Seleccione al menos un (1) framework"})
        fase = fase[0]
        imagen = request.FILES['imagen']


        try:
            print(PosiblesPermisos.MASTER)
            proyecto = Proyecto.objects.get(nombre=nombre)
            proyecto.generos = generos
            proyecto.fase = fase
            proyecto.descripcion = descripcion
            proyecto.frameworks = frameworks
            proyecto.enlace_video = enlace_video
            proyecto.enlace_juego = enlace_descargar
            proyecto.imagen = imagen
            proyecto.save()
        except IntegrityError as e:
            print(e)
            return render(request, "proyectos/crearProyecto.html", {
                "message": "Nombre de proyecto ya registrado"})
        return HttpResponseRedirect(reverse("index"))
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
    proyecto = Proyecto.objects.get(nombre=nombre)
    participaciones = {}
    for participacion in proyecto.participaciones.all():
                roles_p = ""
                for rol in participacion.roles:
                    roles_p= roles_p + " " + str(PosiblesRoles.labels[PosiblesRoles.values.index(rol)])
                participaciones[participacion.usuario.username] = roles_p
    return render(request,"proyectos/gestionMiembros.html",{
        "proyecto": proyecto,
        "miembros": participaciones
    } )

def agregarMiembros (request, nombre):
    if request.method == "POST" and 'Agregar' in request.POST: 
        roles = request.POST.getlist("roles")
        nom_us = request.POST["nuevoMiembro"]
        nuevo_usuario = Usuario.objects.get(username=nom_us) 

        try:
            proyecto = Proyecto.objects.get(nombre=nombre)
            participacion = Participacion(usuario=nuevo_usuario,proyecto=proyecto,roles=roles,permiso=PosiblesPermisos.MIEMBRO)
            participacion.save()
            return HttpResponseRedirect(reverse("gestionMiembros", kwargs={"nombre": nombre})) 
        except IntegrityError as e:
            print(e)
            return render(request, "proyectos/crearProyecto.html", {
                "message": "Error en la actualización de miembro"}) 
    else:
        try:
            proyecto = Proyecto.objects.get(nombre=nombre)
            personas = []
            for auxPersonas in proyecto.participaciones.all():
                personas.append(auxPersonas.usuario)
            queryset = request.GET.get("buscar")
            usuarios = Usuario.objects.all()
            if queryset:
                usuarios= Usuario.objects.filter(
                    username__icontains=queryset
                )
            

            return render(request,"proyectos/agregarMiembros.html",{
                "miembros": personas,
                "proyecto": proyecto,
                "usuarios": usuarios,
                "posiblesroles": PosiblesRoles
                
            } )
        except Proyecto.DoesNotExist:
            return render(request, "main/error.html", {
                "mensaje": "Proyecto no encontrado."
            })
            
def eliminarMiembros (request, nombre):
    if request.method == "POST" and 'Eliminar' in request.POST: 
        nom_us = request.POST["eliminarMiembro"]
        nuevo_usuario = Usuario.objects.get(username=nom_us) 

        try:
            proyecto = Proyecto.objects.get(nombre=nombre)
            participacion = Participacion.objects.get(usuario = nuevo_usuario)
            participacion.delete()
            return HttpResponseRedirect(reverse("gestionMiembros", kwargs={"nombre": nombre})) 
        except IntegrityError as e:
            print(e)
            return render(request, "proyectos/crearProyecto.html", {
                "message": "Error en la actualización de miembro"}) 
    else:
        try:
            proyecto = Proyecto.objects.get(nombre=nombre)
            personas = []
            for auxPersonas in proyecto.participaciones.all():
                if auxPersonas.permiso !=  PosiblesPermisos.MASTER:
                    personas.append(auxPersonas.usuario)      
            usuarios = Usuario.objects.all()
            

            return render(request,"proyectos/eliminarMiembros.html",{
                "miembros": personas,
                "proyecto": proyecto,
                "usuarios": usuarios
                
            } )
        except Proyecto.DoesNotExist:
            return render(request, "main/error.html", {
                "mensaje": "Proyecto no encontrado."
            })

def agregarAdministrador (request, nombre):
    if request.method == "POST" and 'Agregar' in request.POST: 
        nom_us = request.POST["nuevoAdmin"]
        nuevo_usuario = Usuario.objects.get(username=nom_us) 

        try:
            proyecto = Proyecto.objects.get(nombre=nombre)
            participacion = Participacion.objects.get(usuario=nuevo_usuario)
            participacion.permiso = PosiblesPermisos.ADMIN
            participacion.save()
            return HttpResponseRedirect(reverse("gestionMiembros", kwargs={"nombre": nombre})) 
        except IntegrityError as e:
            print(e)
            return render(request, "proyectos/crearProyecto.html", {
                "message": "Error en la actualización de miembro"}) 
    else:
        try:
            proyecto = Proyecto.objects.get(nombre=nombre)
            personas = []
            for auxPersonas in proyecto.participaciones.all():
                if auxPersonas.permiso !=  PosiblesPermisos.MASTER and auxPersonas.permiso !=  PosiblesPermisos.ADMIN:
                    personas.append(auxPersonas.usuario)
            usuarios = Usuario.objects.all()
            

            return render(request,"proyectos/agregarAdministrador.html",{
                "miembros": personas,
                "proyecto": proyecto,
                "usuarios": usuarios,
                "posiblesroles": PosiblesRoles
                
            } )
        except Proyecto.DoesNotExist:
            return render(request, "main/error.html", {
                "mensaje": "Proyecto no encontrado."
            })       

def eliminarAdministrador (request, nombre):
    if request.method == "POST" and 'Eliminar' in request.POST: 
        nom_us = request.POST["eliminarAdmin"]
        nuevo_usuario = Usuario.objects.get(username=nom_us) 

        try:
            proyecto = Proyecto.objects.get(nombre=nombre)
            participacion = Participacion.objects.get(usuario=nuevo_usuario)
            participacion.permiso = PosiblesPermisos.MIEMBRO
            participacion.save()
            return HttpResponseRedirect(reverse("gestionMiembros", kwargs={"nombre": nombre})) 
        except IntegrityError as e:
            print(e)
            return render(request, "proyectos/crearProyecto.html", {
                "message": "Error en la actualización de miembro"}) 
    else:
        try:
            proyecto = Proyecto.objects.get(nombre=nombre)
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
            proyecto.galeria.append(imagen)
            proyecto.save()
        else:
            imagen=None
        descripcion = request.POST['descripcionActualizacion']
    try:
        actualizacion = Actualizacion(proyecto=proyecto,descripcion=descripcion,imagen=imagen)
        actualizacion.save()
    except IntegrityError as e:
            return HttpResponseRedirect(reverse("proyecto",kwargs={"nombre": nombre}))
    return HttpResponseRedirect(reverse("proyecto",kwargs={"nombre": nombre}))