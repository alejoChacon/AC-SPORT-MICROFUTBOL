from django.urls import path
from . import views

urlpatterns = [
    path("api/inscripcion/",views.IncripcionEquipoATorneo.as_view(),name="inscripcionequipoatorneo"),
]