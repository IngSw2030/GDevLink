from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render
from django.http import HttpResponse

def login(request):
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
    if request.method == "POST" and 'registro' in request.POST:
        return render(request,"usuarios/registro.html")
    return render(request, "usuarios/login.html")

def logout(request):
    logout(request)
    return render(request,"login",{
        "message": "Sesion cerrada"
    })
    return HttpResponse("Login")

def registrar(request):
    return render(request,"usuarios/registro.html")

