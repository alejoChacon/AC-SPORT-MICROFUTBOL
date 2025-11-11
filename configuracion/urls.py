from django.urls import path
from . import views

urlpatterns = [
    path("configuracion/",views.Configuracion.as_view(),name="configuracion")
]