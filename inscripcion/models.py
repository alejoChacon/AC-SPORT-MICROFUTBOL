from django.db import models

# Create your models here.

class Inscripcion(models.Model):
    ESTADOS_INSCRIPCION = [
        ('pendiente', 'Pendiente'),
        ('aceptado', 'Aceptado'),
        ('rechazado', 'Rechazado'),
    ]

    torneo = models.ForeignKey('Torneo.Torneo',on_delete=models.CASCADE,related_name='inscripciones')
    equipo = models.ForeignKey('Torneo.Equipo',on_delete=models.CASCADE,related_name='inscripciones_torneo')
    fecha_inscripcion = models.DateTimeField(auto_now_add=True)
    estado = models.CharField(max_length=50,choices=ESTADOS_INSCRIPCION,default='pendiente')
    observaciones = models.TextField(null=True,blank=True)

    #Documentacion requerida
    pago_comprobante = models.ImageField(upload_to='comprobantes_pago/')
    documento_identidad = models.FileField(upload_to='documentos_inscripcion/')

    class Meta:
        verbose_name = "Inscripción a Torneo"
        verbose_name_plural = "Inscripciones a Torneos"
        unique_together = ["torneo","equipo"]
        ordering = ["fecha_inscripcion"]

    def __str__(self):
        return f"{self.equipo.nombre} en proceso de solicitud de inscripcion {self.torneo.nombre}"
