from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render
from django.http import HttpResponse
from proyectos.models import Proyecto, Usuario, Actualizacion
from django.core.paginator import Paginator
from posicionVacante.models import PosicionVacante

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
               vacantes = []
               #fase = PosiblesFases.labels[PosiblesFases.values.index(proyecto.fase)]
               for r in rolesUser:
                    vacantes = vacantes + list(PosicionVacante.objects.filter(roles__contains=[r])) 
          except Actualizacion.DoesNotExist:
               actualizaciones = []
          return render(request,"main/index.html",{
               "actualizaciones": pagina,
               "pagina_anterior": pagina_anterior,
               "pagina_siguiente": pagina_siguiente,
               "vacantes": vacantes
          })
     else:
          todos = Proyecto.objects.all().order_by('seguidores')
          vacantes = PosicionVacante.objects.all()
          populares = [None] * 4
          i=0
          for pop in todos:
               populares[i] = pop
               if i == 3:
                    break
               i = i+1
                
          return render(request,"main/index.html",{"populares": populares, "vacantes": vacantes})