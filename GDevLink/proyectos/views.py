from django.shortcuts import render
from main.enum import *
from proyectos.models import Proyecto, Participacion
from datetime import datetime
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
# Create your views here.

def proyectosUsuario(request):
    if request.user.is_authenticated:
       if request.user.participaciones:
           proyectos = {}
           #for p in request.user.participaciones.proyecto:
            #   proyectos.append(p)
           print(request.user.participaciones.participaciones)
        
           return render(request,"proyectos/proyectosUsuario.html")

       #else
    #else
    
@login_required
def crearProyecto(request):
    if(not request.user.is_authenticated):
        return render(request,"usuarios/login.html")
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

@login_required
def proyecto(request):
    if(not request.user.is_authenticated):
        return render(request,"usuarios/login.html")
    if request.method == "POST":
        return render(request,"proyectos/proyecto.html",{})
    return render(request,"proyectos/proyecto.html",{})