from django.urls import path
from . import views
from . import api

urlpatterns = [
    path('programacion/',views.ProgramacionOrganizador.as_view(),name='programacion'),

    # Apis
    path('api/torneos-en-juego/',api.MisTorneosEnJuego.as_view(),name='mistorneosenjuego'),
    path('api/jornadas/<int:torneo_id>/',api.Jornadas.as_view(),name='numeroJornadasTorneo'),
    path('api/partidos/<int:torneo_id>/<int:jornada>/',api.PartidosPorJornadas.as_view(),name='partido_por_jornada'),
    path('api/partido-agenda/',api.AgendarPartido.as_view(),name='agendarpartido'),
]