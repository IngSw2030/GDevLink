from django.contrib import admin
from proyectos.models import Proyecto, Participacion, Actualizacion
# Register your models here.
admin.site.register(Proyecto)
admin.site.register(Participacion)
admin.site.register(Actualizacion)
