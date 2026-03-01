from django.db import models
from django.core.validators import MinValueValidator,MaxValueValidator

# Create your models here.

class Equipo(models.Model):
    escudo = models.ImageField(upload_to="escudo_equipo",blank=False,null=False)
    nombre = models.CharField(max_length=50,unique=True)
    fecha_creacion = models.DateField(auto_now_add=True)
    fecha_update = models.DateTimeField(auto_now=True)
    municipio = models.CharField(max_length=50,help_text="Municipio del equipo",blank=False,null=False)
    capitan = models.OneToOneField("usuarios.Usuario",on_delete=models.SET_NULL, null=True,blank=True)
    activo = models.BooleanField(default=True)

    class Meta:
        verbose_name = "Equipo"
        verbose_name_plural = "Equipos"

    def __str__(self):
        return self.nombre
    
class Torneo(models.Model):
    # Estados posibles del torneo
    ESTADOS_TORNEO = [
        ('inscripcion', 'Inscripción'),
        ('programado', 'Programado'),
        ('en_curso', 'En Curso'),
        ('finalizado', 'Finalizado'),
        ('cancelado', 'Cancelado'),
    ]
    # Formatos de torneo
    FORMATOS_TORNEO = [
        ('liga', 'Liga Todos contra Todos'),
        ('eliminacion', 'Eliminación Directa'),
        ('grupos', 'Fase de Grupos + Eliminación'),
    ]
    #campos basicos
    logo_torneo = models.ImageField(upload_to="LogoTorneo/")
    nombre = models.CharField(max_length=100,unique=True)
    descripcion = models.TextField(blank=True)
    # Información de organización
    representante = models.CharField(max_length=100)
    celular_contacto = models.CharField(max_length=10)
    email_contacto = models.EmailField(blank=True,default='agudelochacon@gmail.com')
    #Configuracion del torneo
    formato = models.CharField(max_length=50,choices=FORMATOS_TORNEO,default='grupos')
    estado = models.CharField(max_length=50,choices=ESTADOS_TORNEO,default='inscripcion')
    max_equipos = models.PositiveIntegerField(default=30,validators=[MinValueValidator(15),MaxValueValidator(30)])
    #fechas importantes
    fecha_inicio_inscripcion = models.DateField()
    fecha_fin_inscripcion = models.DateField()
    fecha_inicio_torneo = models.DateField(null=True,blank=True)
    fecha_fin_torneo = models.DateField(null=True,blank=True)
    #Campos Automaticos
    fecha_creacion = models.DateField(auto_now_add=True)
    fecha_actualizacion = models.DateTimeField(auto_now=True)
    jugadores_por_equipo = models.PositiveSmallIntegerField(default=10)

    @property
    def equipos_inscritos(self):
        """ Cantidad de equipos inscritos en el torneo """
        return self.inscripciones.filter(estado='aceptado').count()
    
    @property
    def inscripciones_abiertas(self):
        """ Verifica si las inscripciones están abiertas"""
        from django.utils import timezone
        hoy = timezone.now().date()
        return (self.estado == "inscripcion" and self.fecha_inicio_inscripcion <= hoy <= self.fecha_fin_inscripcion)

    def puede_inscribir_equipos(self):
        """ Verifica si todavía hay cupos disponibles para inscribirse al torneo """
        return self.inscripciones_abiertas and self.equipos_inscritos < self.max_equipos

    class Meta:
        verbose_name = "Torneo"
        verbose_name_plural = "Torneos"
        ordering = ["-fecha_creacion"]

    def __str__(self):
        return f"{self.nombre} ({self.get_estado_display()})"
