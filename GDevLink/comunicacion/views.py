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
from usuarios.ManejadorUsuarios import ManejadorUsuarios

# Create your views here.


@login_required(login_url='/usuarios/inicio-sesion')
def conversaciones(request):
     if request.method == "POST":
          usuarioB = request.POST.getlist('usuarioB')
          if usuarioB:
               conv = ManejadorComunicacion.agregarConversacion(request.user.username, usuarioB[0])
               if conv is None:
                    return render(request, "main/error.html", {
                         "mensaje": "Ocurrió un error."
                    })
               return redirect('conversaciones/'+ str(conv.id) + '/chat/')

          return HttpResponseRedirect(reverse("conversaciones"))
     elif request.method == "GET":
          result_list = list(Usuario.objects.all().values('username'))
          dataJSON = dumps(result_list) 
          conversaciones = list(ManejadorComunicacion.obtenerConversaciones(request.user.username))
          usuarios = ManejadorUsuarios.obtenerUsuarios()
          for con in conversaciones:
               if list(con.mensajes.all()):
                    print (list(con.mensajes.all())[-1].texto)
          return render(request,"comunicacion/conversaciones.html", {'users': dataJSON, 'conversaciones': conversaciones,"usuarios":usuarios})
     
  

@login_required(login_url='/usuarios/inicio-sesion')
def chat(request, room_name):
     if request.method == "GET":
          conversacion = ManejadorComunicacion.obtenerMensajes(request.user.username, room_name)
          conversaciones = ManejadorComunicacion.obtenerConversaciones(request.user.username)
          return render(request, "comunicacion/chat.html", {
                    "conversacion": conversacion, 'room_name': room_name, 'conversaciones': conversaciones})
