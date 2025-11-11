from django.urls import path
from . import views 

urlpatterns = [
    path("",views.PageStart.as_view(),name="inicio"),
    path("xxx/",views.Plataforma.as_view(),name="plataforma"),
    path("AC-MICRO-SPORT/",views.Inicio.as_view(),name="plataforma_inicio")
]