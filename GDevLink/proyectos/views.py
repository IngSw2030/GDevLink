from django.shortcuts import render
from main.enum import *
from proyectos.models import Proyecto, Participacion
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
        imagen = request.POST['imagen']

        try:
            print(PosiblesPermisos.MASTER)
            proyecto = Proyecto(nombre=nombre,generos=generos,fase=fase,descripcion=descripcion,frameworks=frameworks,enlace_video=enlace_video, imagen=imagen)
            proyecto.save()
        except IntegrityError as e:
            print(e)
            return render(request, "proyectos/crearProyecto.html", {
                "message": "Nombre de proyecto ya registrado"})
        try:
            participacion= Participacion(usuario=request.user,proyecto=proyecto,roles=roles,permiso=PosiblesPermisos.MASTER)
            participacion.save()
            return HttpResponseRedirect(reverse("proyecto", kwargs={"nombre": nombre}))
        except IntegrityError as e:
            print(e)
            return render(request, "proyectos/crearProyecto.html", {
                "message": "Error en la creacion de participacion"})
    return render(request,"proyectos/crearProyecto.html",{"generos":PosiblesGeneros ,"fases":PosiblesFases ,"frameworks":PosiblesFrameworks,"roles":PosiblesRoles})

def proyecto(request,nombre):
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
        return render(request, "proyectos/proyecto.html", {
            "proyecto": proyecto,
            "generos": generos,
            "miembros": participaciones,
            "frameworks": frameworks,
            "fase": fase
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

