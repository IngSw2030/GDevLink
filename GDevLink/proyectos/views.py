from django.shortcuts import render
from main.enum import *
from proyectos.models import Proyecto, Participacion
from datetime import datetime
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
# Create your views here.

def proyectosUsuario(request):
    if request.user.is_authenticated():
        pass
       #if not request.user.Participacion
       #if not request.user.Participacion
       #return render(request,"proyectos/proyectosUsuario.html",{"proyectos": request.user.Proyecto})

       #else
    #else
    
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
        

        if(nombre == ""):
            return render(request,"proyectos/crearProyecto.html",{"generos":PosiblesGeneros ,"fases":PosiblesFases ,"frameworks":PosiblesGeneros,
             "message": "Por favor ingresar un nombre"})
       # if(len(fase)!=1):
        #    return render(request,"proyectos/crearProyecto.html",{"generos":PosiblesGeneros ,"fases":PosiblesFases ,"frameworks":PosiblesGeneros,
         #    "message": "Seleccione una (1) fase"})
        #if(len(frameworks)==0):
         #   return render(request,"proyectos/crearProyecto.html",{"generos":PosiblesGeneros ,"fases":PosiblesFases ,"frameworks":PosiblesGeneros,
          #   "message": "Seleccione al menos un (1) framework"})
        #imagenes = UploadImageForm(request.POST, request.FILES)      
        #enlace_juego = 
        try:
            proyecto = Proyecto(nombre=nombre,generos=generos,fase=fase,descripcion=descripcion,frameworks=frameworks,enlace_video=enlace_video)
            proyecto.save()

            participacion= Participacion(usuario=request.user,proyecto=proyecto,roles=roles,permiso=PosiblesPermisos.MASTER)
            participacion.save()
        except IntegrityError as e:
            print(e)
            return render(request, "proyectos/crearProyecto.html", {
                "message": "Nombre de proyecto ya registrado"})
    return render(request,"proyectos/crearProyecto.html",{"generos":PosiblesGeneros ,"fases":PosiblesFases ,"frameworks":PosiblesGeneros})