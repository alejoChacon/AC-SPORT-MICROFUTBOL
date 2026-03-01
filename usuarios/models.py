from django.db import models
from django.contrib.auth.models import AbstractUser
from Torneo.models import Equipo
from django.templatetags.static import static

# Create your models here.

class Usuario(AbstractUser):
    foto = models.ImageField(upload_to="foto_perfil",null=True,blank=True)
    fecha_nacimiento = models.DateField(null=True)
    documento = models.CharField(max_length=100,choices=[
        ("C.C","Cédula de ciudadania"),
        ("P.S","Pasaporte"),
        ("T.I","Tarjeta de identidad")],default="C.C")
    num_document = models.CharField(max_length=15,unique=True)
    celular = models.CharField(max_length=10,unique=True)
    equipos = models.ForeignKey(Equipo,on_delete=models.SET_NULL,null=True,blank=True,related_name='jugadores')
    posicion = models.CharField(max_length=50,
                                choices=[("arquero","ARQUERO"),("cierre","CIERRE"),("ala","ALA"),("pívot","PIVOT")],
                                blank=True,null=True)
    numero_camisa = models.PositiveIntegerField(null=True,blank=True)

    @property
    def get_foto_url(self):
        if self.foto:
            return self.foto.url
        else:
            return static('img/sin-foto.jpg')

    class Meta:
        verbose_name = "Usuario"
        verbose_name_plural = "Usuarios"

    def __str__(self):
        return self.get_full_name()