from django.shortcuts import render
from main.enum import *
from main.enum import Framework, Genero, Rol, Permiso, Fases
from proyectos.models import Proyecto, Participacion, Usuario, Actualizacion
from posicionVacante.models import PosicionVacante
from datetime import datetime
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.urls import reverse
from django.http import HttpResponse, HttpResponseRedirect
from posicionVacante.ManejadorVacantes import ManejadorVacantes
from proyectos.ManejadorProyectos import ManejadorProyectos


@login_required(login_url='/usuarios/inicio-sesion')
def gestion_vacantes(request, nombre):
    if request.method == "GET":
        vacantes = ManejadorVacantes.obtenerVacantesProyecto(nombre)
        proyecto = ManejadorProyectos.obtenerProyecto(nombre)
        return render(request, "posicionVacante/gestionVacantes.html", {
            "proyecto": proyecto,
            "vacantes": vacantes,
            "posiblesFrameworks": Framework,
            "posiblesRoles": Rol})

def nueva_vacante(request, nombre):
    if request.method == "POST":
        roles = request.POST.getlist("roles")
        frameworks = request.POST.getlist('frameworks')
        descripcion = request.POST.get('descripcion', False)
        proyecto = ManejadorProyectos.obtenerProyecto(nombre)
        vacante = ManejadorVacantes.crearVacante(nombre, roles, frameworks, descripcion)
        if vacante is not None:
            proyecto = vacante.proyecto
            return HttpResponseRedirect(reverse("gestion-vacantes", kwargs={"nombre": proyecto.nombre}))
        else:
            return render(request, "main/error.html", {
                        "mensaje": "Ocurrió un error."
                })

def vacante(request, ids):
    if request.method == "POST":
        if request.POST.get("request") == "DELETE":
            vacante = ManejadorVacantes.obtenerVacante(ids)
            if vacante is None:
                return render(request, "main/error.html", {
                        "mensaje": "Ocurrió un error."
                })
            proyecto = vacante.proyecto
            if ManejadorVacantes.eliminarVacante(ids) == -1:
                return render(request, "main/error.html", {
                        "mensaje": "Ocurrió un error."
                })
            return HttpResponseRedirect(reverse("gestion-vacantes", kwargs={"nombre": proyecto.nombre}))
        elif request.POST.get("request") == "PUT":
            roles=[]
            frameworks=[]
            roles = request.POST.getlist("roles")
            frameworks = request.POST.getlist('frameworks')
            descripcion = request.POST.get('descripcion')
            if len(frameworks)==0:
                return render(request, "main/error.html", {
                    "mensaje": "Debe seleccionar al menos (1) framework."
                })
            if len(roles)==0:
                return render(request, "main/error.html", {
                    "mensaje": "Debe seleccionar al menos (1) rol."
                })
            vacante = ManejadorVacantes.editarVacante(ids, roles, frameworks, descripcion)
            if vacante is None:
                return render(request, "main/error.html", {
                    "mensaje": "Ocurrió un error."
                })
            else:
                proyecto = vacante.proyecto
                return HttpResponseRedirect(reverse("gestion-vacantes", kwargs={"nombre": proyecto.nombre}))
            
def aplicantes(request, ids):
    if request.method == "PUT":
        if ManejadorVacantes.aplicarVacante(request.user.username, ids) == 0:
            return HttpResponse(status=200)
        else:
            return render(request, "main/error.html", {
                "mensaje": "Ocurrió un error."
            })
    elif request.method == "GET":
        vacante = ManejadorVacantes.obtenerVacante(ids)
        if vacante is None:
            return render(request, "main/error.html", {
                "mensaje": "Ocurrió un error."
            })
        proyecto = vacante.proyecto
        aplicantes = ManejadorVacantes.obtenerAplicantes(ids)
        if aplicantes is None:
            return render(request, "main/error.html", {
                "mensaje": "Ocurrió un error."
            })
        return render(request, "posicionVacante/listaAplicantes.html", {
            "vacante": vacante,
            "aplicantes": aplicantes,
            "proyecto":proyecto,
            "posiblesRoles": Rol,
            "posiblesFrameworks": Framework
        })

def explorarVacantes(request):
    if request.method == "POST":
        nombre_busqueda = request.POST['barraBusqueda']
        roles = request.POST.getlist("roles")
        frameworks = request.POST.getlist('frameworks')
        vacantes = ManejadorVacantes.buscarVacantes(nombre_busqueda, roles, frameworks)
        return render(request, "posicionVacante/explorarVacantes.html", {
            "posicionesVacantes": vacantes,
            "posiblesRoles": Rol,
            "posiblesFrameworks": Framework
        })
    elif request.method == "GET":
        vacantes = []
        vacantes = PosicionVacante.objects.all()

        return render(request, "posicionVacante/explorarVacantes.html", {
            "posicionesVacantes": vacantes,
            "posiblesRoles": Rol,
            "posiblesFrameworks": Framework
        })

def editarVacante(request,ids):
    vacante = ManejadorVacantes.obtenerVacante(ids)
    if vacante is None:
        return render(request, "main/error.html", {
                "mensaje": "Ocurrió un error."
            })
    proyecto = vacante.proyecto
    return render(request, "posicionVacante/editarVacante.html", {
        "proyecto": proyecto,
        "vacante": vacante,
        "posiblesFrameworks": Framework,
        "posiblesRoles": Rol
    })