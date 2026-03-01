from django.contrib import admin
from .models import Partido
from Torneo.models import Torneo as Charala

# Register your models here.

class EditarAdminPartido(admin.ModelAdmin):

    list_display = ("grupo","jornada","equipo_local",'goles_local','goles_visitante',"equipo_visitante",'estado',"fecha_hora")
    ordering = ('-torneo',)

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "torneo":
            kwargs["queryset"] = Charala.objects.filter(estado="en_curso")
        return super().formfield_for_foreignkey(db_field, request, **kwargs)

admin.site.register(Partido,EditarAdminPartido)
