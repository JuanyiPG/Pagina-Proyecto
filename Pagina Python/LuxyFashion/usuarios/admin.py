from django.contrib import admin
from .models import Rol, Usuario, Empleado, Cliente

admin.site.register(Rol)
admin.site.register(Usuario)
admin.site.register(Empleado)
admin.site.register(Cliente)