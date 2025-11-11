from django.contrib import admin
from .models import Grupo,EquipoGrupo
from Torneo.models import Torneo,Equipo

# Register your models here.

class UptomizeGroup(admin.ModelAdmin):

    list_display = ("torneo","nombre")

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "torneo":
            kwargs["queryset"] = Torneo.objects.filter(estado="en_curso")
        return super().formfield_for_foreignkey(db_field, request, **kwargs)
    
class UptomizerEquipoGrupo(admin.ModelAdmin):

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "equipo":
            kwargs["queryset"] = Equipo.objects.filter(participacion_grupo__isnull=True)
        return super().formfield_for_foreignkey(db_field, request, **kwargs)

admin.site.register(Grupo,UptomizeGroup)
admin.site.register(EquipoGrupo,UptomizerEquipoGrupo)