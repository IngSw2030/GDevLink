from django.shortcuts import render
from main.enum import *
from proyectos.models import Proyecto, Participacion, Usuario, Actualizacion
from datetime import datetime
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.urls import reverse
from django.http import HttpResponse, HttpResponseRedirect
# Create your views here.

@login_required
def lobby(request):
     return render(request,"comunicacion/lobby.html")

@login_required
def conversaciones(request):
    return render(request,"comunicacion/conversaciones.html")