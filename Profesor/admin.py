from django.contrib import admin
from .models import Profesor
from Clase.models import Clase

admin.site.register(Profesor)

# borrar esto cuando se termine el módulo de clases es para poder probar el módulo de profesores sin tener que crear clases desde el admin
admin.site.register(Clase)
