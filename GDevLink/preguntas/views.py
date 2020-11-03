from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.urls import reverse
from django.http import HttpResponse, HttpResponseRedirect
from preguntas.models import Usuario, Pregunta, Respuesta

def preguntas(request):
    preguntas=Pregunta.objects.all()
    return render(request,"preguntas/preguntas.html",{"preguntas":preguntas})

@login_required(login_url='/usuarios/login')
def crearPregunta(request):
    preguntas=Pregunta.objects.all()
    if request.method == "POST":
        titulo = request.POST["titulo"]
        texto = request.POST["texto"]
        if(titulo == ""):
            return render(request,"preguntas/crearPregunta.html",{"preguntas":preguntas,
             "message": "Por favor ingresar el titulo de la pregunta"})
        if(texto == ""):
            return render(request,"preguntas/crearPregunta.html",{"preguntas":preguntas,
             "message": "Por favor ingresar la descripcion de la pregunta"})
        result=Pregunta.objects.filter(titulo=titulo).count()
        if result > 0:
            return render(request,"preguntas/crearPregunta.html",{"preguntas":preguntas,
             "message": "Titulo de la pregunta ya existe"})
        try:
            pregunta=Pregunta(titulo=titulo,texto=texto,autor=request.user)
            pregunta.save()
            preguntas=Pregunta.objects.all()
            return render(request, "preguntas/crearPregunta.html",{"preguntas":preguntas})
        except IntegrityError as e:
            print(e)
            return render(request,"preguntas/crearPregunta.html",{"preguntas":preguntas,
             "message": "Titulo de la pregunta ya existe"})
    return render(request, "preguntas/crearPregunta.html",{"preguntas":preguntas})