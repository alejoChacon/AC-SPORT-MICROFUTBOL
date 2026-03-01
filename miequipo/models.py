from django.db import models
from django.core.exceptions import ValidationError

# Create your models here.

class Alineacion(models.Model):
    equipo = models.OneToOneField('Torneo.Equipo',on_delete=models.CASCADE,related_name='titular_equipo')
    portero = models.ForeignKey('usuarios.Usuario',on_delete=models.SET_NULL,null=True,related_name="titular_arquero")
    cierre = models.ForeignKey('usuarios.Usuario',on_delete=models.SET_NULL,null=True,related_name="titular_cierre")
    ala_izq = models.ForeignKey('usuarios.Usuario',on_delete=models.SET_NULL,null=True,related_name="titular_alaizquierda")
    ala_der = models.ForeignKey('usuarios.Usuario',on_delete=models.SET_NULL,null=True,related_name="titular_aladerecha")
    pivot = models.ForeignKey('usuarios.Usuario',on_delete=models.SET_NULL,null=True,related_name="titular_pivot")
    fecha_update = models.DateTimeField(auto_now=True)

    def clean(self):
        jugadores = [self.portero,self.cierre,self.ala_izq,self.ala_der,self.pivot]
        jugadores_reales = [j.id for j in jugadores if j is not None]
        if len(jugadores_reales) != len(set(jugadores_reales)):
            raise ValidationError('No puede haber dos jugadores repetidos ')

    def __str__(self):
        return f'Equipo titular de {self.equipo.nombre}'