from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.urls import reverse
from django.shortcuts import redirect
from django.http import HttpResponse, HttpResponseRedirect
from preguntas.models import Usuario, Pregunta, Respuesta
from django.db.models import Count

def preguntas(request):
    preguntas=Pregunta.objects.all().annotate(puntos=Count('puntosPositivos') - Count('puntosNegativos')).order_by('-puntos')
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
            respuestas=pregunta.respuestas.all()
            preguntaPos=False
            preguntaNeg=False
            autor=True
            return render(request,"preguntas/verPregunta.html",{
            "pregunta":pregunta, "respuestas":respuestas, 
            "puntosPregunta":pregunta.puntos_positivos()-pregunta.puntos_negativos(),
            "preguntaPos":preguntaPos, "preguntaNeg":preguntaNeg,
            "autor":autor})
        except IntegrityError as e:
            print(e)
            return render(request,"preguntas/crearPregunta.html",{"preguntas":preguntas,
             "message": "Error al crear la pregunta"})
    return render(request, "preguntas/crearPregunta.html",{"preguntas":preguntas})

def verPregunta(request,ids):
    try:
        pregunta=Pregunta.objects.get(id=ids)
        usuario = Usuario.objects.get(username=request.user.get_username())
        respuestasOrdenadas=pregunta.respuestas.annotate(puntos=Count('puntosPositivos') - Count('puntosNegativos')).order_by('-puntos')
        respuestas=[]
        for r in respuestasOrdenadas:
            mejorRespuesta=None
            mR=False
            if pregunta.mejorRespuesta == r:
                    mR=True
            if usuario.respuestasPuntosPositivos.filter(id = r.id):
                rp=True
            else:
                rp=False
            if usuario.respuestasPuntosNegativos.filter(id = r.id):
                rn=True
            else:
                rn=False
            respuesta={"respuesta":r,"mejorRespuesta":mR,"positivo":rp,"negativo":rn}
            respuestas.append(respuesta)

        if usuario.preguntasPuntosPositivos.filter(id = ids):
            preguntaPos = True
            preguntaNeg = False
        else:
            preguntaPos = False
            if usuario.preguntasPuntosNegativos.filter(id = ids):
                preguntaNeg = True
            else:
                preguntaNeg = False
        if usuario == pregunta.autor:
            autor=True
        else:
            autor=False
        return render(request,"preguntas/verPregunta.html",{
            "pregunta":pregunta, "respuestas":respuestas,
            "puntosPregunta":pregunta.puntos_positivos()-pregunta.puntos_negativos(),
            "preguntaPos":preguntaPos, "preguntaNeg":preguntaNeg,
            "autor":autor})
    except Pregunta.DoesNotExist:
        return HttpResponseRedirect(reverse("preguntas"))

@login_required(login_url='/usuarios/login')
def crearRespuesta(request,ids):
    pregunta=Pregunta.objects.get(id=ids)
    respuestas=pregunta.respuestas.all()
    usuario = Usuario.objects.get(username=request.user.get_username())
    if usuario.preguntasPuntosPositivos.filter(id = ids):
            preguntaPos = True
            preguntaNeg = False
    else:
        preguntaPos = False
        if usuario.preguntasPuntosNegativos.filter(id = ids):
            preguntaNeg = True
        else:
            preguntaNeg = False
    if request.method == "POST":
        texto = request.POST['texto']
    try:
        respuesta = Respuesta(texto=texto,pregunta=pregunta,autor=request.user)
        respuesta.save()

        pregunta=Pregunta.objects.get(id=ids)
        usuario = Usuario.objects.get(username=request.user.get_username())
        respuestasOrdenadas=pregunta.respuestas.annotate(puntos=Count('puntosPositivos') - Count('puntosNegativos')).order_by('-puntos')
        respuestas=[]
        for r in respuestasOrdenadas:
            mejorRespuesta=None
            mR=False
            if pregunta.mejorRespuesta == r:
                    mR=True
            if usuario.respuestasPuntosPositivos.filter(id = r.id):
                rp=True
            else:
                rp=False
            if usuario.respuestasPuntosNegativos.filter(id = r.id):
                rn=True
            else:
                rn=False
            respuesta={"respuesta":r,"mejorRespuesta":mR,"positivo":rp,"negativo":rn}
            respuestas.append(respuesta)

        if usuario.preguntasPuntosPositivos.filter(id = ids):
            preguntaPos = True
            preguntaNeg = False
        else:
            preguntaPos = False
            if usuario.preguntasPuntosNegativos.filter(id = ids):
                preguntaNeg = True
            else:
                preguntaNeg = False
        if usuario == pregunta.autor:
            autor=True
        else:
            autor=False        
        return render(request,"preguntas/verPregunta.html",{
            "pregunta":pregunta, "respuestas":respuestas,
            "puntosPregunta":pregunta.puntos_positivos()-pregunta.puntos_negativos(),
            "preguntaPos":preguntaPos, "preguntaNeg":preguntaNeg,
            "autor":autor})
    except IntegrityError as e:
        pregunta=Pregunta.objects.get(id=ids)
        usuario = Usuario.objects.get(username=request.user.get_username())
        respuestasOrdenadas=pregunta.respuestas.annotate(puntos=Count('puntosPositivos') - Count('puntosNegativos')).order_by('-puntos')
        respuestas=[]
        for r in respuestasOrdenadas:
            mejorRespuesta=None
            mR=False
            if pregunta.mejorRespuesta == r:
                    mR=True
            if usuario.respuestasPuntosPositivos.filter(id = r.id):
                rp=True
            else:
                rp=False
            if usuario.respuestasPuntosNegativos.filter(id = r.id):
                rn=True
            else:
                rn=False
            respuesta={"respuesta":r,"mejorRespuesta":mR,"positivo":rp,"negativo":rn}
            respuestas.append(respuesta)

        if usuario.preguntasPuntosPositivos.filter(id = ids):
            preguntaPos = True
            preguntaNeg = False
        else:
            preguntaPos = False
            if usuario.preguntasPuntosNegativos.filter(id = ids):
                preguntaNeg = True
            else:
                preguntaNeg = False
        if usuario == pregunta.autor:
            autor=True
        else:
            autor=False
        return render(request,"preguntas/verPregunta.html",{
            "pregunta":pregunta, "respuestas":respuestas,
            "puntosPregunta":pregunta.puntos_positivos()-pregunta.puntos_negativos(),
            "preguntaPos":preguntaPos, "preguntaNeg":preguntaNeg,
            "autor":autor})


def puntuarPreguntaPos(request,ids):
    if request.method == 'PUT':
        print("si")
        pregunta=Pregunta.objects.get(id=ids)
        usuario = Usuario.objects.get(username=request.user.get_username())
        if usuario in pregunta.puntosPositivos.all():
            pregunta.puntosPositivos.remove(usuario)
        else:
            pregunta.puntosPositivos.add(usuario)
        if usuario in pregunta.puntosNegativos.all():
            pregunta.puntosNegativos.remove(usuario)
        pregunta.save()
    return HttpResponse(status=200)

def puntuarPreguntaNeg(request,ids):
    if request.method == 'PUT':
        pregunta=Pregunta.objects.get(id=ids)
        usuario = Usuario.objects.get(username=request.user.get_username())
        if usuario in pregunta.puntosNegativos.all():
            pregunta.puntosNegativos.remove(usuario)
        else:
            pregunta.puntosNegativos.add(usuario)
        pregunta.save()
        if usuario in pregunta.puntosPositivos.all():
            pregunta.puntosPositivos.remove(usuario)
    return HttpResponse(status=200)

def seleccionarMejorRespuesta(request,ids):
    if request.method == 'PUT':
        respuesta=Respuesta.objects.get(id=ids)
        pregunta=respuesta.pregunta
        idp=pregunta.id
        if pregunta.mejorRespuesta is None:
            pregunta.mejorRespuesta=respuesta
        else:
            if pregunta.mejorRespuesta.id == respuesta.id:
                pregunta.mejorRespuesta=None
            else:
                pregunta.mejorRespuesta=respuesta
        pregunta.save()
    return HttpResponse(status=200)

def puntuarRespuestaPos(request,ids):
    if request.method == 'PUT':
        respuesta=Respuesta.objects.get(id=ids)
        usuario = Usuario.objects.get(username=request.user.get_username())
        if usuario in respuesta.puntosPositivos.all():
            respuesta.puntosPositivos.remove(usuario)
        else:
            respuesta.puntosPositivos.add(usuario)
        respuesta.save()
        if usuario in respuesta.puntosNegativos.all():
            respuesta.puntosNegativos.remove(usuario)
    return HttpResponse(status=200)

def puntuarRespuestaNeg(request,ids):
    if request.method == 'PUT':
        respuesta=Respuesta.objects.get(id=ids)
        usuario = Usuario.objects.get(username=request.user.get_username())
        if usuario in respuesta.puntosNegativos.all():
            respuesta.puntosNegativos.remove(usuario)
        else:
            respuesta.puntosNegativos.add(usuario)
        respuesta.save()
        if usuario in respuesta.puntosPositivos.all():
            respuesta.puntosPositivos.remove(usuario)
    return HttpResponse(status=200)
