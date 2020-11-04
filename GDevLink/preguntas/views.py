from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.urls import reverse
from django.http import HttpResponse, HttpResponseRedirect
from preguntas.models import Usuario, Pregunta, Respuesta

def preguntas(request):
    preguntas=Pregunta.objects.all().order_by('-puntosPositivos')
    return render(request,"preguntas/preguntas.html",{"preguntas":preguntas})

@login_required(login_url='/usuarios/login')
def crearPregunta(request):
    preguntas=Pregunta.objects.all().order_by('-puntosPositivos')
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
            preguntas=Pregunta.objects.all().order_by('-puntosPositivos')
            respuestas=pregunta.respuestas.all()
            return render(request, "preguntas/verPregunta.html",{"pregunta":pregunta,"respuestas":respuestas})
        except IntegrityError as e:
            print(e)
            return render(request,"preguntas/crearPregunta.html",{"preguntas":preguntas,
             "message": "Error al crear la pregunta"})
    return render(request, "preguntas/crearPregunta.html",{"preguntas":preguntas})

def verPregunta(request,ids):
    preguntas=Pregunta.objects.all().order_by('-puntosPositivos')
    try:
        pregunta=Pregunta.objects.get(id=ids)
        respuestas=pregunta.respuestas.all()
        len(pregunta.puntosPositivos.all())
        return render(request,"preguntas/verPregunta.html",{
            "pregunta":pregunta, "respuestas":respuestas, 
            "pPuntosPositivos":len(pregunta.puntosPositivos)})
    except Pregunta.DoesNotExist:
        return HttpResponseRedirect(reverse("preguntas"))
    return HttpResponseRedirect(reverse("preguntas"))

@login_required(login_url='/usuarios/login')
def crearRespuesta(request,ids):
    if request.method == "POST":
        pregunta=Pregunta.objects.get(id=ids)
        texto = request.POST['texto']
    try:
        respuesta = Respuesta(texto=texto,pregunta=pregunta,autor=request.user)
        respuesta.save()
        pregunta=Pregunta.objects.get(id=ids)
        respuestas=pregunta.respuestas.all()
        return render(request,"preguntas/verPregunta.html",{"pregunta":pregunta, "respuestas":respuestas})
    except IntegrityError as e:
        pregunta=Pregunta.objects.get(id=ids)
        respuestas=pregunta.respuestas
        return render(request,"preguntas/verPregunta.html",{"pregunta":pregunta, "respuestas":respuestas})
    pregunta=Pregunta.objects.get(id=ids)
    respuestas=pregunta.respuestas
    return render(request,"preguntas/verPregunta.html",{"pregunta":pregunta, "respuestas":respuestas})