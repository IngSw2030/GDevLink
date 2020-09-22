from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
def index(request):
    return HttpResponse("Hello, world!")

def login(request):
    return HttpResponse("Login")

def registrar(request):
    return HttpResponse("Registro")