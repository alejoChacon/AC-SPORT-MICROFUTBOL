from django.db import models

# Create your models here.

class NotificacionSolicitud(models.Model):
    receptor = models.ForeignKey('usuarios.Usuario',on_delete=models.CASCADE,related_name='notificaciones')
    remitente = models.ForeignKey('usuarios.Usuario',on_delete=models.CASCADE,related_name='remitente_notificaion')
    equipo = models.ForeignKey('Torneo.Equipo',on_delete=models.CASCADE,related_name='notificaion_equipo')
    accion = models.BooleanField(default=False)
    leida = models.BooleanField(default=False)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    informacion = models.CharField(max_length=50,null=True)

    class Meta:
        ordering = ['-fecha_creacion']
