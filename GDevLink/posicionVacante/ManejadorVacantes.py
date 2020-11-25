from posicionVacante.models import PosicionVacante
from posicionVacante.IManejadorVacantes import IManejadorVacantes
from proyectos.ManejadorProyectos import ManejadorProyectos
from usuarios.ManejadorUsuarios import ManejadorUsuarios
from django.db import IntegrityError
from main.enum import Framework, Genero, Rol, Permiso, Fases

#Clase que implementa la interfaz IManejadorVacantes
class ManejadorVacantes(IManejadorVacantes):
    def obtenerVacante(idVacante):
        #Se intenta obtener la vacante
        try:
            vacante = PosicionVacante.objects.get(id=idVacante)
            return vacante
        #Se retorna None si no existe
        except PosicionVacante.DoesNotExist as e:
            return None
    
    def crearVacante(nombreProyecto, roles, frameworks, descripcion):
        #Se obtiene el proyecto
        proyecto = ManejadorProyectos.obtenerProyecto(nombreProyecto)
        #Si el proyecto no existe, se retorna None
        if proyecto is None:
            return None
        #Se intenta crear la posición vacante
        try:
            posicion = PosicionVacante(
                roles=roles, frameworks=frameworks, descripcion=descripcion, proyecto=proyecto)
            posicion.save()
            return posicion
        #Se retorna None si ocurre algún error en la creación
        except IntegrityError as e:
            return None
    
    def editarVacante(idVacante, roles, frameworks, descripcion):
        #Se intenta obtener la vacante y guardar las modificaciones
        try:
            vacante = PosicionVacante.objects.get(id=idVacante)
            vacante.roles=roles
            vacante.frameworks=frameworks
            vacante.descripcion=descripcion
            vacante.save()
            return vacante
        #Se retorna None si ocurre algún error
        except (IntegrityError,PosicionVacante.DoesNotExist) as e:
            return None
    
    def eliminarVacante(idVacante):
        try:
            PosicionVacante.objects.get(id=idVacante).delete()
            return 0
        #Se retorna None si ocurre algún error
        except (IntegrityError,PosicionVacante.DoesNotExist) as e:
            return -1
    
    def buscarVacantes(nombreProyecto, roles, frameworks):  
        if nombreProyecto != '':
            return PosicionVacante.objects.filter(

                roles__contains=roles,

                frameworks__contains=frameworks,

                proyecto__icontains=nombreProyecto
            )
        else:
            return PosicionVacante.objects.filter(

                roles__contains=roles,

                frameworks__contains=frameworks,
            )
    
    def aplicarVacante(nombreUsuario, idVacante):
        try:
            usuario = ManejadorUsuarios.obtenerUsuario(nombreUsuario)
            if usuario is None:
                return -1
            vacante = PosicionVacante.objects.get(id=idVacante)
            vacante.aplicantes.add(usuario)
            vacante.save()
            return 0
        except PosicionVacante.DoesNotExist as e:
            return -1

    def obtenerVacantesProyecto(nombreProyecto):
        proyecto = ManejadorProyectos.obtenerProyecto(nombreProyecto)
        if proyecto is not None:
            return proyecto.vacantes.all()
        else:
            return None

    def obtenerAplicantes(idVacante):
        try:
            vacante = PosicionVacante.objects.get(id=idVacante)
            return vacante.aplicantes.all()
        except PosicionVacante.DoesNotExist as e:
            return None
    
    def obtenerVacantesSugeridas(nombreUsuario):
        usuario = ManejadorUsuarios.obtenerUsuario(nombreUsuario)
        rolesUser = usuario.roles
        vacantesRepetidas = []
        for r in rolesUser:
            vacantesRepetidas = vacantesRepetidas + list(PosicionVacante.objects.filter(roles__contains=[r]))
        vacantesCodigo = list(dict.fromkeys(vacantesRepetidas))
        vacantes = {}
        for vac in vacantesCodigo:
            roles_p = ""
            #Para cada participacion se recorren sus roles
            for rol in vac.roles:
                    #Todos los roles son concatenados
                    roles_p= roles_p + " " + str(Rol.labels[Rol.values.index(rol)])
            #String es agregado a la lista de participaciones, en la posición del usuario
            vacantes[vac.proyecto.nombre] = roles_p
        return vacantes