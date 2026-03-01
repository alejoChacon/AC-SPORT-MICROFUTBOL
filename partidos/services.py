from django.shortcuts import get_object_or_404
from Torneo.models import Torneo
from .models import Partido
from datetime import datetime
from django.utils import timezone

hoy = timezone.now()

def obtener_partidos_por_jornadas(torneo_id,jornada):
    torneo = get_object_or_404(Torneo,pk=torneo_id)
    partidos_por_jornada = torneo.partidos.filter(jornada=jornada)
    data = []
    for partido in partidos_por_jornada:
        data.append({
            'id':partido.pk,
            'estado':partido.estado,
            'nombre_equipo_local': partido.equipo_local.nombre,
            'escudo_equipo_local': partido.equipo_local.escudo.url,
            'nombre_equipo_visitante': partido.equipo_visitante.nombre,
            'escudo_equipo_visitante': partido.equipo_visitante.escudo.url,
            'fecha': partido.fecha_hora if partido.fecha_hora else 'Sin asignar',
            'cancha': partido.cancha if partido.cancha else 'Sin cancha'
        })
    return data

def fixture_agendarpartidos(partido_id,fecha,hora,cancha):
    try:
        partido = get_object_or_404(Partido,pk=partido_id)

        # convertimos a objetos date y time
        fecha = datetime.strptime(fecha,'%Y-%m-%d').date()
        #hora = datetime.strptime(hora,'%H:%M:%S').time() #me dice que esta llegando una hora así 18:00, sin segundos (06:00 p.m)
        hora = datetime.strptime(hora,'%H:%M').time()

        #Combinamos
        fecha_hora = datetime.combine(fecha,hora)
        partido.fecha_hora = fecha_hora
        partido.cancha = cancha
        partido.estado = 'programado'
        partido.save()
        return 'Partido programado con exito'
    except Exception as e:
        print('Error: ',str(e))

def partidos_de_hoy(torneo_id):
    torneo = get_object_or_404(Torneo,pk=torneo_id)
    partidos_hoy = torneo.partidos.filter(fecha_hora__date=hoy.date())
    return partidos_hoy
    