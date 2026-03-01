from django.shortcuts import get_object_or_404
from django.db.models import Count,Q,Max
from .models import Equipo, Torneo
from partidos.models import Partido
from fase_de_grupos.models import Grupo,EquipoGrupo
from django.db import transaction
from django.utils import timezone
import random

hoy = timezone.now()

def generar_grupos_torneo(torneo_id, cantidad_grupos):
    equipos_ids = list(Equipo.objects.filter(
        inscripciones_torneo__estado='aceptado',
        inscripciones_torneo__torneo__pk=torneo_id
    ).values_list('id',flat=True))
    if not equipos_ids:
        raise ValueError('No hay equipos aceptados para este Torneo')
    random.shuffle(equipos_ids)
    name_groups = ['A','B','C','D','E','F','G','H']
    #with transaction.atomic():
    Grupo.objects.filter(torneo_id=torneo_id).delete()
    objeto_grupo = []
    for i in range(cantidad_grupos):
        grupo = Grupo.objects.create(nombre = name_groups[i],torneo_id = torneo_id)
        objeto_grupo.append(grupo)
    for turno,equipo in enumerate(equipos_ids):
        # Usamos el operador % (Módulo). Es como dar vueltas en círculo.
                # Si hay 3 grupos, el resultado siempre será 0, 1 o 2.
                # Turno 0 % 3 = 0 (Va al Grupo A)
                # Turno 1 % 3 = 1 (Va al Grupo B)
                # Turno 2 % 3 = 2 (Va al Grupo C)
                # Turno 3 % 3 = 0 (¡Vuelve al Grupo A!) -> Así se llenan parejos.
        letra_grupo = objeto_grupo[turno % cantidad_grupos]
        EquipoGrupo.objects.create(
            grupo = letra_grupo,
            equipo_id = equipo
        )
    torneo = Torneo.objects.get(pk=torneo_id)
    torneo.estado = 'en_curso'
    torneo.save()
    return torneo

def obtener_estado_incripcion(user,torneo):
    #Con el getattr, lo que se hace es tomar el valor del aributo de la clase.
    user_equipo = getattr(user, 'equipos', None) 
    if not user_equipo:
        return {'esta_inscrito':False,'pendiente':False}
    
    print(torneo.inscripciones.filter(equipo=user_equipo,estado='pendiente').exists())

    #Logica de negocio
    return{
        'esta_inscrito': torneo.inscripciones.filter(equipo=user_equipo,estado='aceptado').exists(),
        'inscripcion_pendiente': torneo.inscripciones.filter(equipo=user_equipo,estado='pendiente').exists()
    }

def equiposInscritos(torneo_pk):
    try:
        torneo = Torneo.objects.get(pk=torneo_pk)
        equipos_inscritos = Equipo.objects.filter(inscripciones_torneo__estado='aceptado',inscripciones_torneo__torneo=torneo)
        if len(equipos_inscritos) > 0:
            equipos = []
            for equipo in equipos_inscritos:
                equipos.append({
                    'equipo_id': equipo.pk,
                    'foto': equipo.escudo.url if equipo.escudo else '',
                    'nombre': equipo.nombre
                })
            return equipos
        return None
    except Exception as e:
        print('Error: ',str(e))

def cantidad_solicitudes_pendientes(torneo):
    try:
        solicitudes_pendientes = torneo.inscripciones.filter(estado='pendiente')
        return {
            'solicitudes_pendientes':solicitudes_pendientes,
            'cantidad_pendeintes': solicitudes_pendientes.count(),
            'tiempo_inscripcion_caducado': True if torneo.fecha_fin_inscripcion < hoy.date() else False
        } 
    except Exception as e:
        print('Error: ',str(e))

def generar_fixture(torneo_pk):
    """Genera calendario Round Robin para una lista de equipos"""
    
    torneo = get_object_or_404(Torneo,pk=torneo_pk)
    Partido.objects.filter(torneo=torneo).delete()
    cantidad_grupos = torneo.grupo_set.all().distinct()
    #with transaction.atomic():
    for grupo in cantidad_grupos:

        equipos = list(Equipo.objects.filter(participacion_grupo__grupo=grupo))

        # ESTE PRINT TE HABRÍA DICHO: "Equipos encontrados: 0"
        print(f"DEBUG: Grupo {grupo.nombre} - Equipos encontrados: {len(equipos)}") 

        if len(equipos) == 0:
            # Esto lanzaría un error y así la transacción haría Rollback
            raise ValueError(f"El grupo {grupo.nombre} no tiene equipos asignados.")

        if len(equipos) % 2 != 0:
            equipos.append("DESCANSO")
        cantidad_equipos = len(equipos)

        for ronda in range(cantidad_equipos - 1):
            for i in range(cantidad_equipos // 2):
                equipo1 = equipos[i]
                equipo2 = equipos[cantidad_equipos - 1 - i]
                if equipo1 != "DESCANSO" and equipo2 != "DESCANSO":
                    Partido.objects.create(
                        torneo = torneo,
                        equipo_local = equipo1,
                        equipo_visitante = equipo2,
                        grupo = grupo,
                        jornada = ronda + 1,
                    )
            equipos = [equipos[0]] + [equipos[-1]] + equipos[1:-1]

def jornadas_del_torneo(torneo_pk):

    torneo = get_object_or_404(Torneo,pk=torneo_pk)
    data = []

    jornadas = list(torneo.partidos.values_list('jornada',flat=True).order_by('jornada').distinct())
    for jornada in jornadas:
        partido = Partido.objects.filter(torneo=torneo,jornada=jornada).last()
        total_programados = Partido.objects.filter(torneo=torneo,jornada=jornada,estado='programado').count()

        if partido.fecha_hora:
            if partido.fecha_hora.date() == hoy.date():
                estado_jornada = 'En Curso'
            elif partido.fecha_hora > hoy:
                estado_jornada = 'Próximamente'
            elif hoy > partido.fecha_hora:
                estado_jornada = 'Finalizado'
        else:
            estado_jornada = 'Proximamente'

        data.append({
            'jornada': jornada,
            'fecha': partido.fecha_hora,
            'partidos_programados': total_programados,
            'estado': estado_jornada  
        })
        print(f'Jornada: {partido.jornada} | Fecha {partido.fecha_hora} | Total equipos programados {total_programados} | Estado: {estado_jornada}' )

    """resumen_jornadas = torneo.partidos.values('jornada').annotate(
        total_programados=Count('id', filter=Q(estado='programado')),
        fecha=Max('fecha_hora')
    ).order_by('jornada')"""

    return data
    