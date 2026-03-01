from django.shortcuts import get_object_or_404
from Torneo.models import Equipo

def nomina_equipo_local(equipo_pk):
    equipo = get_object_or_404(Equipo,pk=equipo_pk)
    equipo_local = equipo.titular_equipo
    return equipo_local

def nomina_equipo_visitante(equipo_pk):
    equipo = get_object_or_404(Equipo,pk=equipo_pk)
    equipo_visitante = equipo.titular_equipo
    return equipo_visitante