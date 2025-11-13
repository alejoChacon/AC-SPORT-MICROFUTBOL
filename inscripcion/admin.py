from django.contrib import admin
from .models import Inscripcion
from Torneo.models import Torneo,Equipo

# Register your models here.

class UptomizaInscription(admin.ModelAdmin):

    list_display = ("id","torneo","equipo") 
    
    def formfield_for_foreignkey(self,db_field,request,**kwargs):
        if db_field.name == "torneo":
            kwargs["queryset"] = Torneo.objects.filter(estado="inscripcion")
        #elif db_field.name == "equipo":
        #    kwargs["queryset"] = Equipo.objects.filter(inscripciones_torneo=None) 
        return super().formfield_for_foreignkey(db_field, request, **kwargs)

admin.site.register(Inscripcion,UptomizaInscription)
