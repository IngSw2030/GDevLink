from django.shortcuts import render
from main.enum import PosiblesFrameworks, PosiblesGeneros, PosiblesFases
# Create your views here.

def proyectosUsuario(request):
    if request.user.is_authenticated():
       #if not request.user.Participacion
       return render(request,"proyectos/proyectosUsuario.html",{"proyectos": request.user.Proyecto})

       #else
    #else

def crearProyecto(request):
    if request.method == "POST" and 'crearProyecto' in request.POST:
        nombre = request.POST["name"]
        generos = request.POST.getlist("generos")
        fase = request.POST.getlist('fase')
        descripcion = request.POST['descripcion']
        frameworks = request.POST.getlist('frameworks')
        if(nombre == ""):
            return render(request,"proyectos/crearProyecto.html",{"generos":PosiblesGeneros ,"fases":PosiblesFases ,"frameworks":PosiblesGeneros, "message": "Por favor ingresar un nombre"})
        if(len(fase)!=1):
            return render(request,"proyectos/crearProyecto.html",{"generos":PosiblesGeneros ,"fases":PosiblesFases ,"frameworks":PosiblesGeneros, "message": "Seleccione una (1) fase"})
        if(len(frameworks)==0):
            return render(request,"proyectos/crearProyecto.html",{"generos":PosiblesGeneros ,"fases":PosiblesFases ,"frameworks":PosiblesGeneros, "message": "Seleccione al menos un (1)framework"})
        #imagen = 
        #galeria = 
        #enlace_video = 
        #enlace_video = 
        #enlace_juego = 
        #fecha_creacion
    
    return render(request,"proyectos/crearProyecto.html",{"generos":PosiblesGeneros ,"fases":PosiblesFases ,"frameworks":PosiblesGeneros})