from django.contrib import admin
from .models import Usuarios, UsuariosGrupos, GruposPermisos
# Register your models here.
admin.site.register(Usuarios)
admin.site.register(GruposPermisos)
