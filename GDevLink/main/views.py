from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render
from django.http import HttpResponse
from proyectos.models import Proyecto, Usuario, Actualizacion
from django.core.paginator import Paginator
from posicionVacante.models import PosicionVacante
from main.enum import Framework, Genero, Rol, Permiso, Fases
from proyectos.ManejadorProyectos import ManejadorProyectos

# Vista para la página principal
def index(request):
     
     #Si el usuario está autenticado, se le muestran las actualizaciones de los proyectos a los que sigue
     if request.user.is_authenticated:
          #Se obtiene el número de página solicitado
          numero_pagina = int(request.GET.get("numero_pagina", 1))
          #Los valores por defecto de la página anterior y la página siguiente son -1, que indican que no hay más páginas
          pagina_anterior = -1
          pagina_siguiente = -1
          #Se obtiene el usuario
          usuario = Usuario.objects.get(username=request.user.get_username())
          try:
               #Se obtienen las actualizaciones de los proyectos seguidos por el usuario, ordenadas descendentemente por fecha
               actualizaciones = Actualizacion.objects.order_by("-fecha").filter(proyecto__in = usuario.proyectos_seguidos.all())
               #Se dividen los resultados en páginas de 5 actualizaciones
               paginas = Paginator(actualizaciones, 5)
               #Si el número de página solicitada no se encuentra en el rango, se utiliza la primera página
               if numero_pagina not in paginas.page_range:
                    numero_pagina = 1
               #Se obtiene la página
               pagina = paginas.page(numero_pagina)
               #Se revisa si hay página anterior
               if pagina.has_previous():
                    pagina_anterior = numero_pagina - 1
               #Se revisa si hay página siguiente
               if pagina.has_next():
                    pagina_siguiente = numero_pagina + 1
               rolesUser = request.user.roles
     
               vacantesRepetidas = []
               #fase = Fases.labels[Fases.values.index(proyecto.fase)]
               for r in rolesUser:
                    vacantesRepetidas = vacantesRepetidas + list(PosicionVacante.objects.filter(roles__contains=[r]))
    
               vacantesCodigo = list(dict.fromkeys(vacantesRepetidas))
               vacantes = {}
               proyectoKey = {}
               
               for vac in vacantesCodigo:
                    
                    if request.user not in vac.aplicantes.all():
                         roles_p = ""
                         #Para cada vacante se recorren sus roles
                         for rol in vac.roles:
                              #Todos los roles son concatenados
                              roles_p= roles_p + " " + str(Rol.labels[Rol.values.index(rol)])  
                         #String es agregado a la lista de vacantes, en la posición del usuario
                         vacantes[vac.id] = roles_p
                         proyectoKey[vac.id] = vac.proyecto
               
          except Actualizacion.DoesNotExist:
               actualizaciones = []
          return render(request,"main/index.html",{
               "actualizaciones": pagina,
               "pagina_anterior": pagina_anterior,
               "pagina_siguiente": pagina_siguiente,
               "vacantes": vacantes,
               "proyectoKey": proyectoKey
          })
     else:
          
          populares = ManejadorProyectos.obtenerProyectosPopulares()
          vacantesCodigo = list(PosicionVacante.objects.all())
          vacantes = {}
               
          for vac in vacantesCodigo:
               roles_p = ""
               #Para cada participacion se recorren sus roles
               for rol in vac.roles:
                    #Todos los roles son concatenados
                    roles_p= roles_p + " " + str(Rol.labels[Rol.values.index(rol)])
                        
                    #String es agregado a la lista de participaciones, en la posición del usuario
               vacantes[vac.proyecto.nombre] = roles_p
                
          return render(request,"main/index.html",{"populares": populares, "vacantes": vacantes})