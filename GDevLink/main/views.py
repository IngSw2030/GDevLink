from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render
from django.http import HttpResponse
from proyectos.models import Proyecto, Usuario, Actualizacion

# Create your views here.
# Create your views here.
def index(request):
     if request.user.is_authenticated:
          usuario = Usuario.objects.get(username=request.user.get_username())
          try:
               actualizaciones = Actualizacion.objects.order_by("-fecha").filter(proyecto__in = usuario.proyectos_seguidos.all())
          except Actualizacion.DoesNotExist:
               actualizaciones = []
          return render(request,"main/index.html",{
               "actualizaciones": actualizaciones
          })
     else:
          return render(request),"main/index.html"