from django.shortcuts import render

# Create your views here.

def proyectosUsuario(request):
    if request.user.is_authenticated():
       if not request.user.Participacion
       return render(request,"proyectos/proyectosUsuario.html",{"proyectos": request.user.Proyecto})

       else
    else

def crearProyecto():