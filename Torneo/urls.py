from django.urls import path
from . import views
from . import logica

urlpatterns = [
    path("torneo/",views.Torneo.as_view(),name="torneo"),
    path("torneo/<int:pk>/",views.TorneoDetalleView.as_view(),name="detalletorneo"),
    path("torneo/activo/<int:pk>/",views.TorneoActivo.as_view(),name="torneoactivo"),
    path("api/posiciones/<int:torneo_pk>/<str:grupo>/",logica.CargaPosiciones.as_view(),name="torneoposiciones"),
    path("api/resultados/<int:torneo_pk>/<str:grupo>/",logica.CargarResultados.as_view(),name="cargarResultados"),
    path("api/fixture/<int:torneo_pk>/<str:grupo>/",logica.CargarPartidos.as_view(),name="cargarpartidos"),
    path("api/goleador/<int:torneo_pk>/",logica.Goleador.as_view(),name="goleadores")
]