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
        #username=request.POST["username"]
        #password=request.POST["password"]
        #usuario=authenticate(request,username=username, password=password)
        nombre = request.POST["name"]
        generos = request.POST.getlist("generos")
        fase = request.POST.getlist('fase')
        descripcion = request.POST['descripcion']
        frameworks = request.POST.getlist('frameworks')
        enlace_video =request.POST["enlaceVideo"]
        roles = request.POST.getlist("roles")

        for f in frameworks:
            print(len(f))
        for f in generos:
            print(len(f))
        for f in fase:
            print(len(f))
        for f in roles:
            print(len(f))
        

        if(nombre == ""):
            return render(request,"proyectos/crearProyecto.html",{"generos":PosiblesGeneros ,"fases":PosiblesFases ,"frameworks":PosiblesGeneros,"roles":PosiblesRoles,
             "message": "Por favor ingresar un nombre"})
        if(len(fase)!=1):
            return render(request,"proyectos/crearProyecto.html",{"generos":PosiblesGeneros ,"fases":PosiblesFases ,"frameworks":PosiblesGeneros,
             "message": "Seleccione una (1) fase"})
        if(len(frameworks)==0):
            return render(request,"proyectos/crearProyecto.html",{"generos":PosiblesGeneros ,"fases":PosiblesFases ,"frameworks":PosiblesGeneros,
             "message": "Seleccione al menos un (1) framework"})
        #imagenes = UploadImageForm(request.POST, request.FILES)      
        #enlace_juego = 
        try:
            print(PosiblesPermisos.MASTER)
            proyecto = Proyecto(nombre=nombre,generos=generos,fase=fase,descripcion=descripcion,frameworks=frameworks,enlace_video=enlace_video)
            proyecto.save()

            participacion= Participacion(usuario=request.user,proyecto=proyecto,roles=roles,permiso=PosiblesPermisos.MASTER)
            participacion.save()
        except IntegrityError as e:
            print(e)
            return render(request, "proyectos/crearProyecto.html", {
                "message": "Nombre de proyecto ya registrado"})
    return render(request,"proyectos/crearProyecto.html",{"generos":PosiblesGeneros ,"fases":PosiblesFases ,"frameworks":PosiblesGeneros,"roles":PosiblesRoles})

@login_required
def proyecto(request):
    if request.method == "POST":
        return render(request,"proyectos/proyecto.html",{})
    return render(request,"proyectos/proyecto.html",{})


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