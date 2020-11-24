from django.shortcuts import render

from proyectos.models import Proyecto, Participacion, Usuario, Actualizacion
from comunicacion.models import Conversacion, Mensaje
from datetime import datetime
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.urls import reverse
from django.http import HttpResponse, HttpResponseRedirect
from json import dumps
from random import randint
from django.shortcuts import redirect
from comunicacion.ManejadorComunicacion import ManejadorComunicacion
# Create your views here.


@login_required
def conversaciones(request):
     if request.method == "POST":
          usuarioB = request.POST.getlist('usuarioB')

          conv = ManejadorComunicacion.agregarConversacion(request.user.username, usuarioB[0])
          if conv is None:
               return render(request, "main/error.html", {
                    "mensaje": "Ocurrió un error."
               })
          return redirect('conversaciones/'+ str(conv.id) + '/chat/')
     elif request.method == "GET":
          result_list = list(Usuario.objects.all().values('username'))
          dataJSON = dumps(result_list) 
          conversaciones = ManejadorComunicacion.obtenerConversaciones(request.user.username)

  
         
          return render(request,"comunicacion/conversaciones.html", {'users': dataJSON, 'conversaciones': conversaciones})
     
  

@login_required
def chat(request, room_name):
     if request.method == "GET":
          conversacion = ManejadorComunicacion.obtenerMensajes(request.user.username, room_name)
          return render(request, "comunicacion/chat.html", {
                    "conversacion": conversacion, 'room_name': room_name})
