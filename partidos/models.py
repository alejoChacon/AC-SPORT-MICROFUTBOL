from django.db import models
from fase_de_grupos.models import EquipoGrupo,Grupo

# Create your models here.

class Partido(models.Model):
    ESTADOS_PARTIDO = [('programado', 'Programado'),('en_juego', 'En Juego'),('finalizado', 'Finalizado'),('suspendido', 'Suspendido'),('cancelado', 'Cancelado'),]
    FASES_TORNEO = [('grupos', 'Fase de Grupos'),('octavos', 'Octavos de Final'),('cuartos', 'Cuartos de Final'),('semifinal', 'Semifinal'),('tercer_puesto', 'Tercer Puesto'),('final', 'Final'),]
    torneo = models.ForeignKey("Torneo.Torneo",on_delete=models.CASCADE,related_name="partidos")
    # Equipos participantes
    equipo_local = models.ForeignKey('Torneo.Equipo',on_delete=models.CASCADE,related_name='partidos_local')
    equipo_visitante = models.ForeignKey('Torneo.Equipo',on_delete=models.CASCADE,related_name='partidos_visitante')

    # Información del partido
    fase = models.CharField(max_length=20, choices=FASES_TORNEO, default='grupos')
    grupo = models.ForeignKey(Grupo, on_delete=models.CASCADE, null=True, blank=True)
    jornada = models.PositiveIntegerField(help_text="Número de jornada en la fase")

    # Fecha y lugar
    fecha_hora = models.DateTimeField()
    cancha = models.CharField(max_length=100, blank=True, help_text="Nombre de la cancha")

    # Estado y resultado
    estado = models.CharField(max_length=20, choices=ESTADOS_PARTIDO, default='programado')
    goles_local = models.PositiveIntegerField(default=0)
    goles_visitante = models.PositiveIntegerField(default=0)

    #Campo control
    persona_finalizo_partido = models.CharField(max_length=50,blank=True,null=True,help_text="Usuario que registró el resultado")
    fecha_actualizacion = models.DateTimeField(auto_now=True)

    @property
    def ganador(self):
        if self.estado != "finalizado":
            return None
        if self.goles_local > self.goles_visitante:
            return self.equipo_local
        elif self.goles_visitante > self.goles_local:
            return self.equipo_visitante
        return None #empate
    
    @property
    def perdedor(self):
        if self.estado != "finalizado":
            return None
        if self.goles_local < self.goles_visitante:
            return self.equipo_local
        elif self.goles_visitante < self.goles_local:
            return self.equipo_visitante
        return None
    
    @property
    def es_empate(self):
        return self.estado == 'finalizado' and self.goles_local == self.goles_visitante
    
    def resultado_texto(self):
        if self.estado != 'finalizado':
            return f"{self.get_estado_display()}"
        return f"{self.goles_local} - {self.goles_visitante}"
    
    def actualizar_estadisticas(self):
        """Actualiza las estadísticas de los equipos en el grupo"""

        if self.grupo and self.estado == "finalizado":
            #Actuaizar estadisticas del equipo local
            equipo_grupo_local = EquipoGrupo.objects.get(grupo=self.grupo,equipo=self.equipo_local)
            equipo_grupo_local.partidos_jugados += 1
            equipo_grupo_local.goles_favor += self.goles_local
            equipo_grupo_local.goles_contra += self.goles_visitante

            if self.ganador == self.equipo_local:
                equipo_grupo_local.partidos_ganados =+ 1
                equipo_grupo_local.puntos += 3
            elif self.es_empate:
                equipo_grupo_local.puntos += 1
                equipo_grupo_local.partidos_empatados += 1
            else:
                equipo_grupo_local.partidos_perdidos += 1
            equipo_grupo_local.save() 

            equipo_grupo_visitante = EquipoGrupo.objects.get(grupo=self.grupo,equipo=self.equipo_visitante)
            equipo_grupo_visitante.partidos_jugados += 1
            equipo_grupo_visitante.goles_favor += self.goles_visitante
            equipo_grupo_visitante.goles_contra += self.goles_local

            if self.ganador == self.equipo_visitante:
                equipo_grupo_visitante.partidos_ganados += 1
                equipo_grupo_visitante.puntos += 3
            elif self.es_empate:
                equipo_grupo_visitante.partidos_empatados += 1
                equipo_grupo_visitante.puntos += 1
            else:
                equipo_grupo_visitante.partidos_perdidos += 1
            equipo_grupo_visitante.save()

    class Meta:
        verbose_name = "Partido"
        verbose_name_plural = "Partidos"
        ordering = ['fecha_hora', 'torneo']
        unique_together = [
            ['torneo', 'equipo_local', 'equipo_visitante', 'fase'],
            ['grupo', 'equipo_local', 'equipo_visitante', 'jornada']
        ]

    def save(self,*args,**kwargs):
        
        # Si el partido se marca como finalizado, actualizar estadísticas
        if self.estado == "finalizado" and self.pk:
            old_partido = Partido.objects.get(pk=self.pk)
            if old_partido.estado != "finalizado":
                self.actualizar_estadisticas()

        return super().save(*args,**kwargs)
    
    def __str__(self):
        return f'{self.equipo_local} vs {self.equipo_visitante} - {self.torneo.nombre} - Grupo {self.grupo.nombre}'