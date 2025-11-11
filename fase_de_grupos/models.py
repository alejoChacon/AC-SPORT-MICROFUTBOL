from django.db import models

# Create your models here.

class Grupo(models.Model):
    torneo = models.ForeignKey('Torneo.Torneo',on_delete=models.CASCADE)
    nombre = models.CharField(max_length=1,help_text="A,B,C etc...")
    equipos = models.ManyToManyField('Torneo.Equipo')

    class Meta:
        verbose_name = 'Grupo'
        verbose_name_plural = 'Grupos'
        unique_together = ["torneo","nombre"]

    def __str__(self):
        return f'{self.nombre} {self.torneo.nombre}'
    
class EquipoGrupo(models.Model):
    grupo = models.ForeignKey(Grupo,on_delete=models.CASCADE)
    equipo = models.ForeignKey("Torneo.Equipo",on_delete=models.CASCADE,related_name="participacion_grupo")
    puntos = models.IntegerField(default=0)
    partidos_jugados = models.IntegerField(default=0)
    partidos_jugados = models.IntegerField(default=0)
    partidos_ganados = models.IntegerField(default=0)
    partidos_empatados = models.IntegerField(default=0)
    partidos_perdidos = models.IntegerField(default=0)
    goles_favor = models.IntegerField(default=0)
    goles_contra = models.IntegerField(default=0)
    tarjeta_amarilla = models.IntegerField(default=0)
    tarjeta_roja = models.IntegerField(default=0)
    tarjeta_azul = models.IntegerField(default=0)

    @property
    def diferencias_goles(self):
        return self.goles_favor - self.goles_contra
    
    class Meta:
        unique_together = ['grupo','equipo']
        ordering = ["-puntos"]

    def __str__(self):
        return f'Tabla de poscicion del equipo {self.equipo} para el grupo {self.grupo.nombre}'

    
    