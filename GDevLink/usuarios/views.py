from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.db import IntegrityError
from usuarios.models import Usuario
from main.enum import PosiblesFrameworks, PosiblesGeneros, PosiblesRoles
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django import forms
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserChangeForm, PasswordChangeForm
from django.contrib.auth.decorators import login_required
from usuarios.ManejadorUsuarios import ManejadorUsuarios


def inicio_sesion(request):
    if request.method == "POST" and 'login' in request.POST:
        username = request.POST["username"]
        password = request.POST["password"]
        if ManejadorUsuarios.login(request, username, password) is not None:
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "usuarios/login.html", {
                "message": "Datos de inicio de sesion incorrectos"
            })
    elif request.method == "GET":
        return render(request, "usuarios/login.html")


def cierre_sesion(request):
    if request.method == "GET":
        ManejadorUsuarios.logOut(request)
        return HttpResponseRedirect(reverse("inicio-sesion"))


def registro(request):
    if request.method == "POST":
        # Se obtienen datos de la solicitud
        username = request.POST["username"]
        email = request.POST["email"]
        roles = request.POST.getlist('roles')
        generos = request.POST.getlist('generos')
        frameworks = request.POST.getlist('frameworks')
        # Se revisa que ambas contraseñas coincidan
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "usuarios/registrar.html", {
                "message": "Las contraseñas no coinciden."
            })
        # Se intenta crear el nuevo usuario. En caso de que falle la creación,
        # se le indica al usuario
        user = ManejadorUsuarios.registrar(
            username, email, roles, generos, frameworks, password)
        if user is None:
            return render(request, "usuarios/registrar.html", {
                "message": "Correo o nombre de usuario ya registrado.",
                "roles": PosiblesRoles,
                "generos": PosiblesGeneros,
                "frameworks": PosiblesFrameworks
            })
        login(request, user, backend='django.contrib.auth.backends.ModelBackend')
        return HttpResponseRedirect(reverse("index"))
    elif request.method == "GET":
        return render(request, "usuarios/registrar.html", {
            "roles": PosiblesRoles,
            "generos": PosiblesGeneros,
            "frameworks": PosiblesFrameworks
        })


def perfil(request, nombre_usuario):
    if request.method == "GET":
        usuario = ManejadorUsuarios.obtenerUsuario(nombre_usuario)
        if usuario is None:
            return render(request, "main/error.html", {
                "mensaje": "Usuario no encontrado."
            })
        participaciones = {}
        roles = []
        generos = []
        frameworks = []
        if(usuario.roles is None or usuario.generos is None or usuario.frameworks is None):
            usuario.roles = roles
            usuario.generos = generos
            usuario.frameworks = frameworks
            usuario.save()
        for rol in usuario.roles:
            roles.append(
                (PosiblesRoles.labels[PosiblesRoles.values.index(rol)]))
        for genero in usuario.generos:
            generos.append(
                (PosiblesGeneros.labels[PosiblesGeneros.values.index(genero)]))
        for framework in usuario.frameworks:
            frameworks.append(
                (PosiblesFrameworks.labels[PosiblesFrameworks.values.index(framework)]))
        for participacion in usuario.participaciones.all():
            roles_p = ""
            for rol in participacion.roles:
                roles_p = roles_p + " " + \
                    str(PosiblesRoles.labels[PosiblesRoles.values.index(rol)])
            participaciones[participacion.proyecto.nombre] = roles_p
        autenticado = request.user
        return render(request, "usuarios/perfil.html", {
            "autenticado": autenticado,
            "usuario": usuario,
            "participaciones": participaciones,
            "roles": roles,
            "generos": generos,
            "frameworks": frameworks
        })
    elif request.method == "POST":
        descripcion = request.POST['descripcion']
        roles = request.POST.getlist('roles')
        generos = request.POST.getlist('generos')
        frameworks = request.POST.getlist('frameworks')
        if(len(roles) == 0):
            return render(request, "main/error.html", {
                "mensaje": "Debe seleccionar al menos (1) rol."
            })
        user = ManejadorUsuarios.obtenerUsuario(nombre_usuario)
        # Se revisa que el usuario que va a modificar el perfil sea el dueño del perfil
        if user is None:
            return render(request, "usuarios/editar.html", {
                "message": "Error inesperado"
            })
        if user != request.user:
            return render(request, "main/error.html", {
                "mensaje": "No tiene acceso a este recurso."
            })
        if 'imagen' in request.FILES:
            imagen = request.FILES['imagen']
        else:
            imagen = user.imagen
        user = ManejadorUsuarios.editarPerfil(
            nombre_usuario, roles, generos, frameworks, descripcion, imagen)
        if user is None:
            return render(request, "usuarios/editar.html", {
                "message": "Error inesperado"
            })
        return HttpResponseRedirect(reverse("perfil", kwargs={"nombre_usuario": nombre_usuario}))


def edicion(request, nombre_usuario):
    if request.method == "GET":
        form = PasswordChangeForm(request.user)
        usuario = ManejadorUsuarios.obtenerUsuario(nombre_usuario)
        if usuario is None:
            return render(request, "main/error.html", {
                "mensaje": "Usuario no encontrado."
            })
        # Se revisa que el usuario que va a acceder a la página sea el dueño del perfil
        if usuario != request.user:
            return render(request, "main/error.html", {
                "mensaje": "No tiene acceso a este recurso."
            })
        participaciones = {}
        roles = []
        generos = []
        frameworks = []
        for rol in usuario.roles:
            roles.append(
                (PosiblesRoles.labels[PosiblesRoles.values.index(rol)]))
        for genero in usuario.generos:
            generos.append(
                (PosiblesGeneros.labels[PosiblesGeneros.values.index(genero)]))
        for framework in usuario.frameworks:
            frameworks.append(
                (PosiblesFrameworks.labels[PosiblesFrameworks.values.index(framework)]))
        for participacion in usuario.participaciones.all():
            roles_p = ""
            for rol in participacion.roles:
                roles_p = roles_p + " " + \
                    str(PosiblesRoles.labels[PosiblesRoles.values.index(rol)])
            participaciones[participacion.proyecto.nombre] = roles_p
        return render(request, "usuarios/editar.html", {
            "usuario": usuario,
            "participaciones": participaciones,
            "roles": roles,
            "posiblesRoles": PosiblesRoles,
            "generos": generos,
            "posiblesGeneros": PosiblesGeneros,
            "frameworks": frameworks,
            "posiblesFrameworks": PosiblesFrameworks
        })


def cambio_clave(request):
    if request.method == 'POST':
        form = PasswordChangeForm(user=request.user, data=request.POST)
        if ManejadorUsuarios.cambiarContrasena(request):
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "main/error.html", {
                "mensaje": "Se produjo un error en el cambio de clave. Asegúrate de que tu contraseña cumpla con los requisitos."
            })
    elif request.method == 'POST':
        form = PasswordChangeForm(user=request.user)
        args = {'form': form}
        return render(request, 'usuarios/cambiarClave.html', args)
