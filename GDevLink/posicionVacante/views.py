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


@login_required(login_url='/usuarios/inicio-sesion')
def gestion_vacantes(request, nombre):
    if request.method == "GET":
        proyecto = Proyecto.objects.get(nombre=nombre)
        vacantes = proyecto.vacantes.all()
        return render(request, "posicionVacante/gestionVacantes.html", {
            "proyecto": proyecto,
            "vacantes": vacantes,
            "posiblesFrameworks": PosiblesFrameworks,
            "posiblesRoles": PosiblesRoles})


def nueva_vacante(request, nombre):
    if request.method == "POST":
        proyecto = Proyecto.objects.get(nombre=nombre)
        roles = request.POST.getlist("roles")
        frameworks = request.POST.getlist('frameworks')
        descripcion = request.POST.get('descripcion', False)
        try:
            posicion = PosicionVacante(
                roles=roles, frameworks=frameworks, descripcion=descripcion, proyecto=proyecto)
            posicion.save()
            vacantes = proyecto.vacantes.all()
            return render(request, "posicionVacante/gestionVacantes.html", {
                "proyecto": proyecto,
                "vacantes": vacantes,
                "frameworks": PosiblesFrameworks,
                "roles": PosiblesRoles})
        except IntegrityError as e:
            vacantes = proyecto.vacantes.all()
            return render(request, "posicionVacante/gestionVacantes.html", {
                "proyecto": proyecto,
                "vacantes": vacantes,
                "frameworks": PosiblesFrameworks,
                "roles": PosiblesRoles})
    elif request.method == "GET":
        vacantes = proyecto.vacantes.all()
        return render(request, "posicionVacante/gestionVacantes.html", {
            "proyecto": proyecto,
            "vacantes": vacantes,
            "frameworks": PosiblesFrameworks,
            "roles": PosiblesRoles})



def vacante(request, ids):
    if request.method == "POST":
        if request.POST.get("request") == "DELETE":
            vacante = PosicionVacante.objects.get(id=ids)
            proyecto = vacante.proyecto
            vacante.delete()
            vacantes = proyecto.vacantes.all()
            return HttpResponseRedirect(reverse("gestion-vacantes", kwargs={"nombre": proyecto.nombre}))
        elif request.POST.get("request") == "PUT":
            # Código para modificar vacante
            pass


def aplicantes(request, ids):
    if request.method == "PUT":
        try:

            vacante = PosicionVacante.objects.get(id=ids)
            proyecto = vacante.proyecto
            usuario = Usuario.objects.get(username=request.user)
            vacante.aplicantes.add(usuario)
            vacante.save()
            for aplic in vacante.aplicantes.all():
                print(aplic)
            return HttpResponse(status=200)
        except IntegrityError as e:
            return -1


def explorarVacantes(request):
    if request.method == "POST":
        nombre_busqueda = request.POST['barraBusqueda']
        roles = request.POST.getlist("roles")
        frameworks = request.POST.getlist('frameworks')
        try:    
            if nombre_busqueda != '':
                vacantes = PosicionVacante.objects.filter(

                    roles__contains=roles,

                    frameworks__contains=frameworks,

                    proyecto_icontains=nombre_busqueda
                )
            else:
                vacantes = PosicionVacante.objects.filter(

                    roles__contains=roles,

                    frameworks__contains=frameworks,
                )
        except:
            return render(request, "main/error.html", {
                "mensaje": "la busqueda no existe."})



        return render(request, "posicionVacante/explorarVacantes.html", {
            "posicionesVacantes": vacantes,
            "posiblesRoles": PosiblesRoles,
            "posiblesFrameworks": PosiblesFrameworks
        })

    else:
        vacantes = []
        vacantes = PosicionVacante.objects.all()

        return render(request, "posicionVacante/explorarVacantes.html", {
            "posicionesVacantes": vacantes,
            "posiblesRoles": PosiblesRoles,
            "posiblesFrameworks": PosiblesFrameworks
        })


def listaAplicantes(request, ids):
   
    vacante = PosicionVacante.objects.get(id=ids)
    proyecto = vacante.proyecto
    aplicantes = vacante.aplicantes.all()
    return render(request, "posicionVacante/listaAplicantes.html", {
        "vacante": vacante,
        "aplicantes": aplicantes,
        "proyecto":proyecto,
        "posiblesRoles": PosiblesRoles,
        "posiblesFrameworks": PosiblesFrameworks

    })
     
def editarVacante(request,ids):

    if request.method == "POST" and 'Actualizar' in request.POST:
        
        vacante = PosicionVacante.objects.get(id=ids)
        proyecto = vacante.proyecto
        roles=[]
        frameworks=[]


        try:

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
                  

            vacante.roles=roles
            vacante.frameworks=frameworks
            vacante.descripcion=descripcion
            vacante.save()
            return HttpResponseRedirect(reverse("gestion-vacantes", kwargs={"nombre": proyecto.nombre}))

        except IntegrityError as e:
            return -1
    else:
        vacante = PosicionVacante.objects.get(id=ids)
        proyecto = vacante.proyecto
        return render(request, "posicionVacante/editarVacante.html", {
        "proyecto": proyecto,
        "vacante": vacante,
        "posiblesFrameworks": PosiblesFrameworks,
        "posiblesRoles": PosiblesRoles
        })