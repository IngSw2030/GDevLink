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
                return("index")
            else:
                return render(request, "usuarios/login.html", {
                    "message": "Datos de inicio de sesion incorrectos"
                })
    return render(request, "usuarios/login.html")

def vista_logout(request):
    logout(request)
    return render(request,"login",{
        "message": "Sesion cerrada"
    })
    return HttpResponse("Login")

#def registrar(request):
#    return render(request,"usuarios/registro.html")

def registrar(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]
        roles = request.POST.getlist('roles')
        generos = request.POST.getlist('generos')
        frameworks = request.POST.getlist('frameworks')

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
        


def tasks(request):
    return render(request, "tasks/index.html", {
        "tasks": tasks
    })