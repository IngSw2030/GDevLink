from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.urls import reverse
from django.shortcuts import redirect
from django.http import HttpResponse, HttpResponseRedirect
from preguntas.models import Usuario, Pregunta, Respuesta
from preguntas.ManejadorPreguntas import ManejadorPreguntas
from django.db.models import Count

#Vista principal de las preguntas. 
def preguntas(request):
    if request.method == "GET":
        #Se obtienen las preuntas populares
        preguntas=ManejadorPreguntas.obtenerPreguntasPopulares()
        return render(request,"preguntas/preguntas.html",{"preguntas":preguntas})

#Vista del formulario para crear una pregunta. El usuario debe edtar autentificado.
@login_required(login_url='/usuarios/inicio-sesion')
def crearPregunta(request):
    preguntas=Pregunta.objects.all().order_by('-puntosPositivos')
    if request.method == "POST":
        #Recuperacion de los datos de la pregunta
        titulo = request.POST["titulo"]
        texto = request.POST["texto"]
        #Revision de los parametros de las preguntas
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
        #Creacion de la Pregunta
        pregunta=ManejadorPreguntas.crearPregunta(titulo,texto,request.user.get_username())
        if  pregunta == 1:
            #Si hay un error se retorna mensaje de error
            return render(request,"preguntas/crearPregunta.html",{"preguntas":preguntas,
             "message": "Error al crear la pregunta"})
        #Recuperacion de datos de vista de pregunta
        respuestas=pregunta.respuestas.all()
        preguntaPos=False
        preguntaNeg=False
        autor=True
        #Se redirecciona a la pagina de la pregunta
        return render(request,"preguntas/verPregunta.html",{
        "pregunta":pregunta, "respuestas":respuestas, 
        "puntosPregunta":pregunta.puntos_positivos()-pregunta.puntos_negativos(),
        "preguntaPos":preguntaPos, "preguntaNeg":preguntaNeg,
        "autor":autor})
    elif request.method == "GET":
        #Renderizacion de formulario para crear pregunta
        return render(request, "preguntas/crearPregunta.html",{"preguntas":preguntas})

#Ver la informacion de una Pregunta. Se recibe el id de la pregunta
def verPregunta(request,ids):
    if request.method == "GET":
        #Se busca la pregunta seleccionada
        pregunta=ManejadorPreguntas.verPregunta(ids)
        if  pregunta is None:
            #Si no se encuentra la pregunta se regresa a la pagina inicial de preguntas
            return HttpResponseRedirect(reverse("preguntas"))
        respuestasOrdenadas=pregunta.respuestas.annotate(puntos=Count('puntosPositivos') - Count('puntosNegativos')).order_by('-puntos')
        #Si el usuario esta autentificado se recupera sus datos
        if request.user.is_authenticated:
            usuario = Usuario.objects.get(username=request.user.get_username())
            #Se obtienen las respuestas de la pregunta
            respuestas=obtenerRespuestas(respuestasOrdenadas,pregunta,usuario)
            #Se verifica si la pregunta esta puntuada por el usuario
            if usuario.preguntasPuntosPositivos.filter(id = ids):
                preguntaPos = True
                preguntaNeg = False
            else:
                preguntaPos = False
                if usuario.preguntasPuntosNegativos.filter(id = ids):
                    preguntaNeg = True
                else:
                    preguntaNeg = False
            #Se verifica si el usuario es el autor de la pregunta
            if usuario == pregunta.autor:
                autor=True
            else:
                autor=False
        #Si el usuario no esta autentificado se deja datos por defecto
        else:
            respuestas=obtenerRespuestas(respuestasOrdenadas,pregunta,None)
            preguntaPos = False
            preguntaNeg = False
            autor=False
        return render(request,"preguntas/verPregunta.html",{
            "pregunta":pregunta, "respuestas":respuestas,
            "puntosPregunta":pregunta.puntos_positivos()-pregunta.puntos_negativos(),
            "preguntaPos":preguntaPos, "preguntaNeg":preguntaNeg,
            "autor":autor})

#Vista para crear una respuesta a una pregunta. El usuari
@login_required(login_url='/usuarios/inicio-sesion')
def crearRespuesta(request,ids):
    if request.method == "POST":
        #Datos principales de la vista
        pregunta=Pregunta.objects.get(id=ids)
        respuestas=pregunta.respuestas.all()
        usuario = Usuario.objects.get(username=request.user.get_username())
        #Recuperacion del texto de la respuesta
        if request.method == "POST":
            texto = request.POST['texto']
            #Creacion de la respuesta
            respuesta=ManejadorPreguntas.responderPregunta(ids,texto,request.user.get_username())
            if respuesta == 1:
                pregunta=Pregunta.objects.get(id=ids)
                usuario = Usuario.objects.get(username=request.user.get_username())
                respuestasOrdenadas=pregunta.respuestas.annotate(puntos=Count('puntosPositivos') - Count('puntosNegativos')).order_by('-puntos')
                #Se obtienen las respuestas de la pregunta
                respuestas=obtenerRespuestas(respuestasOrdenadas,pregunta,usuario)
                #Se verifica si la pregunta esta puntuada por el usuario
                if usuario.preguntasPuntosPositivos.filter(id = ids):
                    preguntaPos = True
                    preguntaNeg = False
                else:
                    preguntaPos = False
                    if usuario.preguntasPuntosNegativos.filter(id = ids):
                        preguntaNeg = True
                    else:
                        preguntaNeg = False
                #Se verifica si el usuario es el autor de la pregunta
                if usuario == pregunta.autor:
                    autor=True
                else:
                    autor=False
                return render(request,"preguntas/verPregunta.html",{
                    "pregunta":pregunta, "respuestas":respuestas,
                    "puntosPregunta":pregunta.puntos_positivos()-pregunta.puntos_negativos(),
                    "preguntaPos":preguntaPos, "preguntaNeg":preguntaNeg,
                    "autor":autor})

    #Recuperaciona de datos para la pagina de la pregunta
    pregunta=Pregunta.objects.get(id=ids)
    usuario = Usuario.objects.get(username=request.user.get_username())
    respuestasOrdenadas=pregunta.respuestas.annotate(puntos=Count('puntosPositivos') - Count('puntosNegativos')).order_by('-puntos')
    #Se obtienen las respuestas de la pregunta
    respuestas=obtenerRespuestas(respuestasOrdenadas,pregunta,usuario)
    #Se verifica si la pregunta esta puntuada por el usuario
    if usuario.preguntasPuntosPositivos.filter(id = ids):
        preguntaPos = True
        preguntaNeg = False
    else:
        preguntaPos = False
        if usuario.preguntasPuntosNegativos.filter(id = ids):
            preguntaNeg = True
        else:
            preguntaNeg = False
    #Se verifica si el usuario es el autor de la pregunta
    if usuario == pregunta.autor:
        autor=True
    else:
        autor=False   
    return render(request,"preguntas/verPregunta.html",{
        "pregunta":pregunta, "respuestas":respuestas,
        "puntosPregunta":pregunta.puntos_positivos()-pregunta.puntos_negativos(),
        "preguntaPos":preguntaPos, "preguntaNeg":preguntaNeg,
        "autor":autor})
    
#Vista para Puntuar Positivamente una Pregunta
@login_required(login_url='/usuarios/inicio-sesion')
def puntuarPreguntaPos(request,ids):
    if request.method == 'PUT':
        resultado=ManejadorPreguntas.puntuarPreguntaPos(ids,request.user.get_username())
        if resultado == 1:
            return HttpResponse(status=404)
    return HttpResponse(status=200)

#Vista para Puntuar Negativamente una Pregunta
@login_required(login_url='/usuarios/inicio-sesion')
def puntuarPreguntaNeg(request,ids):
    if request.method == 'PUT':
        resultado=ManejadorPreguntas.puntuarPreguntaNeg(ids,request.user.get_username())
        if resultado == 1:
            return HttpResponse(status=404)
    return HttpResponse(status=200)

#Vista para Seleccionar la mejor respuesta
@login_required(login_url='/usuarios/inicio-sesion')
def seleccionarMejorRespuesta(request,ids):
    if request.method == 'PUT':
        resultado=ManejadorPreguntas.escogerRespuesta(ids)
        if resultado == 1:
            return HttpResponse(status=404)
    return HttpResponse(status=200)
    
#Vista para Puntuar Positivamente una Respuesta
@login_required(login_url='/usuarios/inicio-sesion')
def puntuarRespuestaPos(request,ids):
    if request.method == 'PUT':
        resultado=ManejadorPreguntas.puntuarRespuestaPos(ids,request.user.get_username())
        if resultado == 1:
            return HttpResponse(status=404)
    return HttpResponse(status=200)
    
#Vista para Puntuar Negativamente una Respuesta
@login_required(login_url='/usuarios/inicio-sesion')
def puntuarRespuestaNeg(request,ids):
    if request.method == 'PUT':
        resultado=ManejadorPreguntas.puntuarRespuestaNeg(ids,request.user.get_username())
        if resultado == 1:
            return HttpResponse(status=404)
    return HttpResponse(status=200)

def obtenerRespuestas(respuestasOrdenadas,pregunta,usuario):
    respuestas=[]
    for r in respuestasOrdenadas:
        mejorRespuesta=None
        mR=False
        if pregunta.mejorRespuesta == r:
                mR=True
        if usuario is not None:
            if usuario.respuestasPuntosPositivos.filter(id = r.id):
                rp=True
            else:
                rp=False
            if usuario.respuestasPuntosNegativos.filter(id = r.id):
                rn=True
            else:
                rn=False
        else:
            rp=False
            rn=False
        respuesta={"respuesta":r,"mejorRespuesta":mR,"positivo":rp,"negativo":rn,"autor":r.autor.get_username()}
        respuestas.append(respuesta)
    return respuestas