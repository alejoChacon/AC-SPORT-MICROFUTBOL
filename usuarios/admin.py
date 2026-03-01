from django.contrib import admin
from .models import Usuario

# Register your models here.

class UptomizeUsuario(admin.ModelAdmin):
    list_display = ('id','get_full_name','equipos','posicion')
    list_filter = ('equipos',)
    ordering = ('equipos',)

admin.site.register(Usuario,UptomizeUsuario)
