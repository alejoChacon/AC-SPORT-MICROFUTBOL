from django.urls import path
from . import views
from . import logic

urlpatterns = [
    path("",views.MiEquipo.as_view(),name="miequipo"),
    path("api/equipo_info/<int:equipo_pk>/",views.MiEquipoInfo.as_view(),name="equipoInfo"),
    path("api/calendario-partidos/<int:equipo_pk>/<str:jornada>/",views.CalendarioPartidos.as_view(),name="calendarioPartidos"),
    path("api/searchteam/",logic.SearchTeam.as_view(),name='searchteam'),
]