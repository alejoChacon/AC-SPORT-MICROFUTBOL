from django.db import models
from django.core.validators import MinValueValidator

# Create your models here.

class IncidenciaPartido(models.Model):
    TIPO_EVENTO = [
        ('gol', 'Gol'),
        ('amarilla', 'Tarjeta Amarilla'),
        ('azul', 'Tarjeta Azul'), # Clave en Microfútbol
        ('roja', 'Tarjeta Roja'),
        ('falta', 'Falta Técnica'),
    ]

    partido = models.ForeignKey('partidos.Partido',on_delete=models.CASCADE,related_name='eventos')
    jugador = models.ForeignKey('usuarios.Usuario',on_delete=models.CASCADE)
    tipo = models.CharField(max_length=50,choices=TIPO_EVENTO)
    minuto = models.PositiveSmallIntegerField(MinValueValidator(0))
    periodo = models.PositiveSmallIntegerField()

    class Meta:
        ordering = ['periodo','minuto']
