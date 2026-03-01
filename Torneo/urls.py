from django.urls import path
from . import views
from . import logica
from . import views_organizador
from . import ensayo

urlpatterns = [
    #Endpoints Jugadores
    path("torneos/",views.Torneos.as_view(),name="torneo"),
    path("<int:pk>/",views.TorneoEtapaInscripcion.as_view(),name="detalletorneo"),
    path("activo/<int:pk>/",views.TorneoActivo.as_view(),name="torneoactivo"),
    path("programado/<int:pk>/",views.TorneoEtapaProgramado.as_view(),name='torneoprogramado'),

    #Endpoints Organizador
    path('mis-torneos/',views_organizador.MisTorneos.as_view(),name='mistorneos'),
    path('inscripcion/<int:pk>/',views_organizador.ValidacionINscripcion.as_view(),name='inscripcion'),

    #Apis
    path("api/posiciones/<int:torneo_pk>/<str:grupo>/",logica.CargaPosiciones.as_view(),name="torneoposiciones"),
    path("api/resultados/<int:torneo_pk>/<str:grupo>/<int:fecha>/",logica.CargarResultados.as_view(),name="cargarResultados"),
    path("api/fixture/<int:torneo_pk>/<str:grupo>/<int:fecha>/",logica.CargarPartidos.as_view(),name="cargarpartidos"),
    path("api/goleador/<int:torneo_pk>/",logica.Goleador.as_view(),name="goleadores"),
    path('api/torneo-estado/',logica.EstadoTorneo.as_view(),name='estadoTorneo'),
    path('ensayo/',ensayo.Practicadfe.as_view(),name='ensayo')
]