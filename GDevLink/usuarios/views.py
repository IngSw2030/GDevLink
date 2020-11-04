from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.db import IntegrityError
from usuarios.models import Usuario
from main.enum import PosiblesFrameworks, PosiblesGeneros, PosiblesRoles
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django import forms
from django.contrib.auth import update_session_auth_hash
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserChangeForm, PasswordChangeForm
from django.contrib.auth.decorators import login_required


def vista_login(request):
    if request.method == "POST" and 'login' in request.POST:
            username = request.POST["username"]
            password = request.POST["password"]
            user = authenticate(request, username=username, password=password)
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
        login(request, user, backend='django.contrib.auth.backends.ModelBackend')
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "usuarios/registrar.html", {"roles": PosiblesRoles, "generos": PosiblesGeneros, "frameworks": PosiblesFrameworks})


def perfil(request, nombre_usuario):
    try:
        usuario = Usuario.objects.get(username=nombre_usuario)
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


def editar(request, nombre_usuario):
    if request.method == "POST":
        descripcion = request.POST['descripcion']
        roles = request.POST.getlist('roles')
        generos = request.POST.getlist('generos')
        frameworks = request.POST.getlist('frameworks')

        if(len(roles)==0):
            return render(request, "main/error.html", {
            "mensaje": "Debe seleccionar al menos (1) rol."
        })

        user = Usuario.objects.get(username=nombre_usuario)

        if 'imagen' in request.FILES:
            imagen = request.FILES['imagen']
        else:
            imagen=user.imagen


        for f in roles:
            print(f)

        # Attempt to create new user
        try:
            
            user.roles = roles
            user.generos = generos
            user.frameworks = frameworks
            user.descripcion = descripcion
            user.imagen = imagen
            user.save()
        except IntegrityError as e:
            print(e)
            return render(request, "usuarios/editar.html", {
                "message": "Error inesperado"
            })
        return HttpResponseRedirect(reverse("index"))
    else:
        try:
            form = PasswordChangeForm(request.user)
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
        except Usuario.DoesNotExist:
            return render(request, "main/error.html", {
                "mensaje": "Usuario no encontrado."
            })

def visitarPerfil(request,nombre_usuario):
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
        return render(request, "usuarios/visitarPerfil.html", {
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


def cambiarClave(request):
    if request.method == 'POST':
        print("post")
        form = PasswordChangeForm( user=request.user,data=request.POST)

        if form.is_valid():
            print("entro valid")
            form.save()
            update_session_auth_hash(request, form.user)
            #return redirect(reverse('usuarios:perfil'))
        else:
            print("no valid")
            return render(request, "main/error.html", {
                "mensaje": "Se produjo un error en el cambio de clave. Lea las advertencias en cambiar contraseña"
            })
        
        return HttpResponseRedirect(reverse("index"))
        
    else:
        form = PasswordChangeForm(user=request.user)
        args = {'form': form}
        return render(request, 'usuarios/cambiarClave.html', args)