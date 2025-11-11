from django.db import models
from usuarios.models import Usuario

# Create your models here.

#Este modelo se puede usar para Tabla de Goleadores, y mostrar los goles en tiempo real del partido
class Goleador(models.Model):
    TIPO_GOL = [('normal', 'Gol Normal'),('penalti', 'Penalti'),('autogol', 'Autogol'),]
    partido = models.ForeignKey("partidos.Partido",on_delete=models.CASCADE,related_name="goles")
    jugador = models.ForeignKey("usuarios.Usuario",on_delete=models.CASCADE,related_name="goles")
    equipo = models.ForeignKey("Torneo.Equipo",on_delete=models.CASCADE)
    minuto = models.IntegerField(help_text="Minuto de gol")
    tipo_gol = models.CharField(max_length=10, choices=TIPO_GOL, default='normal')
    es_autogol = models.BooleanField(default=False)

    # Para penaltis
    es_penalti = models.BooleanField(default=False)
    fallo_penalti = models.BooleanField(default=False, help_text="Si falló un penalti")

    fecha_registro = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Gol"
        verbose_name_plural = "Goles"
        ordering = ['partido', 'minuto']

    def __str__(self):
        tipo = "autogol" if self.es_autogol else ""
        return f"{self.jugador.get_full_name()} - {self.minuto}'{tipo}"