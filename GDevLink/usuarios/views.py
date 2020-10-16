from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render
from django.http import HttpResponse
from django.db import IntegrityError
from usuarios.models import Usuario
from main.enum import PosiblesFrameworks, PosiblesGeneros, PosiblesRoles
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django import forms

def vista_login(request):
    if request.method == "POST" and 'login' in request.POST:
            username=request.POST["username"]
            password=request.POST["password"]
            user=authenticate(request,username=username, password=password)
            if user is not None:
                login(request, user)
                return HttpResponseRedirect(reverse("index"))
            else:
                return render(request, "usuarios/login.html", {
                    "message": "Datos de inicio de sesion incorrectos"
                })
    return render(request, "usuarios/login.html")

def vista_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse("login"))

def registrar(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]
        roles = request.POST.getlist('roles')
        generos = request.POST.getlist('generos')
        frameworks = request.POST.getlist('frameworks')

        for f in roles:
            print(f)

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "usuarios/registrar.html", {
                "message": "Las contraseñas no coinciden."
            })

        # Attempt to create new user
        try:
            user = Usuario.objects.create_user(username, email, password)
            user.roles = roles
            user.generos = generos
            user.frameworks = frameworks
            user.save()
        except IntegrityError as e:
            print(e)
            return render(request, "usuarios/registrar.html", {
                "message": "Correo o nombre de usuario ya registrado."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "usuarios/registrar.html",{"roles": PosiblesRoles, "generos": PosiblesGeneros, "frameworks": PosiblesFrameworks})
        


def perfil(request,nombre_usuario):
    try:
        usuario = Usuario.objects.get(username=nombre_usuario)
        participaciones = {}
        roles = []
        generos = []
        frameworks = []
        for rol in usuario.roles:
            roles.append((PosiblesRoles.labels[PosiblesRoles.values.index(rol)]))
        for genero in usuario.generos:
            generos.append((PosiblesGeneros.labels[PosiblesGeneros.values.index(genero)]))
        for framework in usuario.frameworks:
            frameworks.append((PosiblesFrameworks.labels[PosiblesFrameworks.values.index(framework)]))
        for participacion in usuario.participaciones.all():
            roles_p = ""
            for rol in participacion.roles:
                roles_p= roles_p + " " + str(PosiblesRoles.labels[PosiblesRoles.values.index(rol)])
            participaciones[participacion.proyecto.nombre] = roles_p
        return render(request, "usuarios/perfil.html", {
            "usuario": usuario,
            "participaciones": participaciones,
            "roles": roles,
            "generos": generos,
            "frameworks": frameworks
        })
    except Usuario.DoesNotExist:
        return render(request, "main/error.html", {
            "mensaje": "Usuario no encontrado."
        })

