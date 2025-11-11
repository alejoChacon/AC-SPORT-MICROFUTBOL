from django.urls import path
from . import views

urlpatterns = [
    path("",views.MiEquipo.as_view(),name="miequipo")
]