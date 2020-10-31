from django.shortcuts import render
from main.enum import *
from proyectos.models import Proyecto, Participacion, Usuario, Actualizacion
from comunicacion.models import Conversacion, Mensaje
from datetime import datetime
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.urls import reverse
from django.http import HttpResponse, HttpResponseRedirect
from json import dumps
from random import randint
# Create your views here.

@login_required
def lobby(request):
     return render(request,"comunicacion/lobby.html")

@login_required
def conversaciones(request):
     if request.method == "POST" and 'crear' in request.POST:
          usuarioB = request.POST.getlist('usuarioB')
          codigo = randint(1000000000, 9999999999)
          conv = Conversacion(codigo = codigo)
          conv.conversaciones.add(request.user)
          conv.conversaciones.add(Usuario.objects.get(username=usuarioB))
          conv.save()

     else:
          result_list = list(Usuario.objects.all().values('username'))
          dataJSON = dumps(result_list) 
          conversaciones = request.user.conversaciones.all()
          #print(conversaciones.Conversacion)
          #participantes = conversaciones.participantes.objects.all()
          for part in conversaciones:
              # print(part.participantes.all())
               for partici in part.participantes.all():
                    print(partici)
          
     return render(request,"comunicacion/conversaciones.html", {'users': dataJSON, 'conversaciones': conversaciones})
  

@login_required
def chat(request, room_name):
     conversacion = Conversacion.objects.get(codigo=room_name)
     return render(request, "comunicacion/chat.html", {
})
