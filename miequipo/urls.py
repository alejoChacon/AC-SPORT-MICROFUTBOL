from django.urls import path
from . import views
from . import logic

urlpatterns = [
    path("",views.MiEquipo.as_view(),name="miequipo"),
    path('update/equipo/<int:pk>/',views.ActualizarEquipo.as_view(),name='editEquipo'),
    #Apis
    path("api/equipo_info/<int:equipo_pk>/",views.MiEquipoInfo.as_view(),name="equipoInfo"),
    path("api/calendario-partidos/<int:equipo_pk>/<str:jornada>/",views.CalendarioPartidos.as_view(),name="calendarioPartidos"),
    path("api/searchteam/",logic.SearchTeam.as_view(),name='searchteam'),
    path('api/alineacion/',logic.AlineacionEquipo.as_view(),name='alineacionInicial'),
    path('leaving/team/',logic.AbandonarEquipo.as_view(),name='abandonarteam'),
    path('api/show/freeplayer/',logic.Agregarjugador.as_view(),name='addplayer')
]