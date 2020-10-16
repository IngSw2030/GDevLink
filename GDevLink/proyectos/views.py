from django.shortcuts import render
from main.enum import *
from proyectos.models import Proyecto, Participacion
from datetime import datetime
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
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
        roles = request.POST.getlist("roles")

        if(nombre == ""):
            return render(request,"proyectos/crearProyecto.html",{"generos":PosiblesGeneros ,"fases":PosiblesFases ,"frameworks":PosiblesGeneros,"roles":PosiblesRoles,
             "message": "Por favor ingresar un nombre"})
        if(len(fase)!=1):
            return render(request,"proyectos/crearProyecto.html",{"generos":PosiblesGeneros ,"fases":PosiblesFases ,"frameworks":PosiblesGeneros,
             "message": "Seleccione una (1) fase"})
        if(len(frameworks)==0):
            return render(request,"proyectos/crearProyecto.html",{"generos":PosiblesGeneros ,"fases":PosiblesFases ,"frameworks":PosiblesGeneros,
             "message": "Seleccione al menos un (1) framework"})
        
        imagen = request.POST['imagen']
        galeria = request.POST.getlist('galeria')

        try:
            print(PosiblesPermisos.MASTER)
            proyecto = Proyecto(nombre=nombre,generos=generos,fase=fase,descripcion=descripcion,frameworks=frameworks,enlace_video=enlace_video, imagen=imagen, galeria=galeria)
            proyecto.save()
        except IntegrityError as e:
            print(e)
            return render(request, "proyectos/crearProyecto.html", {
                "message": "Nombre de proyecto ya registrado"})
        try:
            participacion= Participacion(usuario=request.user,proyecto=proyecto,roles=roles,permiso=PosiblesPermisos.MASTER)
            participacion.save()
        except IntegrityError as e:
            print(e)
            return render(request, "proyectos/crearProyecto.html", {
                "message": "Error en la creacion de participacion"})
    return render(request,"proyectos/crearProyecto.html",{"generos":PosiblesGeneros ,"fases":PosiblesFases ,"frameworks":PosiblesFrameworks,"roles":PosiblesRoles})

def proyecto(request,nombre):
    try:
        proyecto = Proyecto.objects.get(nombre=nombre)
        miembros = []
        for participacion in proyecto.participaciones.all():
            miembros.append(participacion.usuario.username)
        return render(request, "proyectos/proyecto.html", {
            "nombre": proyecto.nombre,
            "descripcion": proyecto.descripcion,
            "generos": proyecto.generos,
            "frameworks": proyecto.frameworks,
            "miembros": miembros,
            "video": proyecto.enlace_video,
            "descarga": proyecto.enlace_juego
        })
    except Proyecto.DoesNotExist:
        return render(request, "main/error.html", {
            "mensaje": "Proyecto no encontrado."
        })

def proyectosUsuario(request):
    print("Etapa Cero")
    if request.user.is_authenticated:
       print("Etapa Uno")
       if request.user.participaciones:
           proyectos = {}
           #for p in request.user.participaciones.proyecto:
            #   proyectos.append(p)
           print(request.user.participaciones)
        
           return render(request,"proyectos/proyectosUsuario.html")
    return render(request,"proyectos/proyectosUsuario.html")
       #else
    #else

