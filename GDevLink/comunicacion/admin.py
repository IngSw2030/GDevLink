from django.contrib import admin
from comunicacion.models import Conversacion, Mensaje
# Register your models here.
admin.site.register(Conversacion)
admin.site.register(Mensaje)