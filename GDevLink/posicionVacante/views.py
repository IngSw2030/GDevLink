from django.shortcuts import render
from main.enum import *
from main.enum import PosiblesFrameworks, PosiblesGeneros, PosiblesRoles, PosiblesPermisos, PosiblesFases
from proyectos.models import Proyecto, Participacion, Usuario, Actualizacion
from posicionVacante.models import PosicionVacante
from datetime import datetime
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.urls import reverse
from django.http import HttpResponse, HttpResponseRedirect


@login_required(login_url='/usuarios/login')
def gestionarVacantes(request,nombre):
    proyecto = Proyecto.objects.get(nombre=nombre)
    vacantes=proyecto.vacantes.all()
    return render(request, "posicionVacante/gestionVacantes.html",{
        "proyecto":proyecto,
        "vacantes":vacantes,
        "frameworks":PosiblesFrameworks,
        "roles":PosiblesRoles})

def nuevaVacante(request, nombre):
    if request.method == "POST":
        proyecto = Proyecto.objects.get(nombre=nombre)
        roles=request.POST.getlist("roles")
        frameworks=request.POST.getlist('frameworks')
        descripcion = request.POST.get('descripcion',False)
    try:
        posicion = PosicionVacante(roles=roles, frameworks=frameworks, descripcion=descripcion, proyecto=proyecto)
        posicion.save()
        vacantes=proyecto.vacantes.all()
        return render(request, "posicionVacante/gestionVacantes.html",{
            "proyecto":proyecto,
            "vacantes":vacantes,
            "frameworks":PosiblesFrameworks,
            "roles":PosiblesRoles})
    except IntegrityError as e:
        vacantes=proyecto.vacantes.all()
        return render(request, "posicionVacante/gestionVacantes.html",{
            "proyecto":proyecto,
            "vacantes":vacantes,
            "frameworks":PosiblesFrameworks,
            "roles":PosiblesRoles})
    vacantes=proyecto.vacantes.all()
    return render(request, "posicionVacante/gestionVacantes.html",{
        "proyecto":proyecto,
        "vacantes":vacantes,
        "frameworks":PosiblesFrameworks,
        "roles":PosiblesRoles})

def editarVacante(request, ids):
    vacante=PosicionVacante.objects.get(id=ids)
    proyecto=vacante.proyecto
    return render(request, "posicionVacante/editarVacante.html",{
        "vacante":vacante,
    })

def eliminarVacante(request, ids):
    vacante=PosicionVacante.objects.get(id=ids)
    proyecto=vacante.proyecto
    vacante.delete()
    vacantes=proyecto.vacantes.all()
    return render(request, "posicionVacante/gestionVacantes.html",{
        "proyecto":proyecto,
        "vacantes":vacantes,
        "frameworks":PosiblesFrameworks,
        "roles":PosiblesRoles})