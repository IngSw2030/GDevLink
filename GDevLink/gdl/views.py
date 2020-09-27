from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
def index(request):
    return HttpResponse("Hello, world!")

def login(request):
    render(request, "gdl/login.html")
    if request.method == "POST":
            username=request.POST["username"]
            password=request.POST["password"]
            user=authenticate(request,username=username, password=password)
            if user is not None:
                login(request, user)
                return("index")
            else:
                return render(request, "gdl/login.html",{
                    "message": "Datos de inicio de sesion incorrectos"
                })
    return HttpResponse("Login")

def logout(request):
    logout(request)
    return render(request,"login",{
        "message": "Sesion cerrada"
    })
    return HttpResponse("Login")

def registrar(request):
    return render(request,"gdl/registro.html")

