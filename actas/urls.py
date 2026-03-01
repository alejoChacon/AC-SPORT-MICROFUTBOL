from django.urls import path
from . import views
from . import api

urlpatterns = [
    path('resultados-actas/',views.VistaResultadosActas.as_view(),name='resultadosactas'),
    path('fechas-torneos/<int:pk>/',views.FechaTorneos.as_view(),name='fechas_torneo'),
    path('partidos-jornada/<int:torneo_pk>/<int:jornada>/',views.VistaRegistrarMarcadores.as_view(),name='registrarmarcador'),
    path('partido-en-vivo/<int:pk>/',views.PartidoEnVivo.as_view(),name='partidoenvivo'),
    path('ver-detalles-partido/<int:pk>/',views.DetallesActa.as_view(),name='detallepartido'),
    path('gestion-acta/<int:pk>/',views.GestionarActa.as_view(),name='gestionActa'),
    path('datos/gestion-acta/',api.GestionActa.as_view(),name='gestioActaPost'),

    #Url de las Apis
    path('api/partido-en-vivo/',api.PeticionIncidenciaPartido.as_view(),name='peticion-partido-en-vivo'),
    path('api/deleting-sucesos-en-vivo/',api.EliminarSucesoDelPartidoEnVivo.as_view(),name='eliminar-sucesosdel-partido'),
    path('api/marcador-en-vivo/<int:partido_pk>/',api.MarcadorEnVivo.as_view(),name='marcador_en_vivo'),
    path('api/saving-acta/game-live/',api.GuardarActa.as_view(),name='save-acta'),
    path('api/incidencia-partido/<int:partido_pk>/',api.SucesosDElPartidoBeforeplaying.as_view(),name='sucesodelpartidoantesdejugar')

]