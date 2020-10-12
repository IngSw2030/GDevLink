from django.shortcuts import render

# Create your views here.

def proyectosUsuario(request):
    if request.user.is_authenticated():
       #if not request.user.Participacion
       if not request.user.Participacion
       return render(request,"proyectos/proyectosUsuario.html",{"proyectos": request.user.Proyecto})

       #else
    #else

def crearProyecto(request):
    if request.method == "POST" and 'crearProyecto' in request.POST:
        nombre = request.POST["name"]
        generos = request.POST.getlist["generos"]
        fase = request.POST.getlist('fase')
        descripcion = request.POST('descripcion')
        frameworks = request.POST.getlist('frameworks')
        #imagen = 
        #galeria = 
        #enlace_video = 
        #enlace_video = 
        #enlace_juego = 
        #fecha_creacion
    return render(request,"proyectos/crearProyecto.html")