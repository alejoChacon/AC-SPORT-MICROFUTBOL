from django.urls import path
from . import views
from . import logica

urlpatterns = [
    path("api/inscripcion/",views.IncripcionEquipoATorneo.as_view(),name="inscripcionequipoatorneo"),
    path('api/validacion-inscripcion/',logica.ConfirmarInscripcion.as_view(),name='confirmacionInscripcion'),
    path('api/equipos-inscritos/<int:torneo_id>/',logica.TorneoEquipoInscrito.as_view(),name='confirmar_inscripcion'),
]