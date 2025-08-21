from django.contrib import admin
from .models import Espacio, Categoria, Nota, Tarea, Presupuesto

admin.site.register(Espacio)
admin.site.register(Categoria)
admin.site.register(Nota)
admin.site.register(Tarea)
admin.site.register(Presupuesto)
