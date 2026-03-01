from django.shortcuts import get_object_or_404
from partidos.models import Partido
from .models import IncidenciaPartido
from GOLEADOR.models import Goleador
from usuarios.models import Usuario
from django.urls import reverse

def obtener_datos_de_la_fecha(torneo_pk,jornada):
    partidos = Partido.objects.filter(torneo__pk=torneo_pk,jornada=jornada)
    return {
        'total_partidos' : partidos.count(),
        'pendientes': partidos.filter(estado='pendiente').count(),
        'finalizados': partidos.filter(estado='finalizado').count(),
        'jornada': partidos.first().jornada,
        'torneo': partidos.first().torneo.nombre
    }

def incidencias_del_partido(partidoPk):
    partido = get_object_or_404(Partido,pk=partidoPk)
    datos = []
    incidencias = partido.eventos.all()
    for incidencia in incidencias:
        datos.append({
            'pk':incidencia.pk,
            'jugador': incidencia.jugador.get_full_name(),
            'tipo': incidencia.tipo,
            'minuto': incidencia.minuto,
            'periodo': incidencia.periodo,
            'equipo': incidencia.jugador.equipos.nombre
        })
    return datos

def incidencia_de_partido_en_vivo(partidoPK,jugadorPk,accion,minuto,periodo,locacion):
    partido = get_object_or_404(Partido,pk=partidoPK)
    incidenciaDelPartido = IncidenciaPartido.objects.create(
        partido_id = partidoPK,
        jugador_id = jugadorPk,
        tipo = accion,
        minuto = minuto,
        periodo = periodo
    )
    if accion == "gol":
        if locacion == 'equipo_casa':
            partido.goles_local += 1
        elif locacion == 'equipo_visitante':
            partido.goles_visitante += 1
        partido.save()

    """datos = []
    incidencias = partido.eventos.all()
    for incidencia in incidencias:
        datos.append({
            'pk':incidencia.pk,
            'jugador': incidencia.jugador.get_full_name(),
            'tipo': incidencia.tipo,
            'minuto': incidencia.minuto,
            'periodo': incidencia.periodo,
            'equipo': incidencia.jugador.equipos.nombre
        })"""
    datos = incidencias_del_partido(partido.pk)
    return datos

def eliminar_incidencia_del_partido(pk,partidoPk=None):
    incidenciadelpartido = get_object_or_404(IncidenciaPartido,pk=pk)
    accion = incidenciadelpartido.tipo
    jugador = incidenciadelpartido.jugador.get_full_name()

    if accion == 'gol':
        partido = get_object_or_404(Partido,pk=partidoPk)
        equipo_del_jugador = incidenciadelpartido.jugador.equipos

        if partido.equipo_local == equipo_del_jugador:
            partido.goles_local -= 1
        else:
            partido.goles_visitante -= 1
        partido.save()

    if incidenciadelpartido:
        incidenciadelpartido.delete()
        datos = incidencias_del_partido(partidoPk)
        
        return f'{accion} de {jugador} eliminado exitosamente',datos
    else:
        return 'Hubo un error en el proceso de eliminar la incidencia del partido'
    
def marcador_en_Vivo(partido_pk):
    partido = get_object_or_404(Partido,pk=partido_pk)
    return {
        'marcador_local': partido.goles_local,
        'marcador_visitante': partido.goles_visitante
    }

def guardarActa(partido_pk):
    partido = get_object_or_404(Partido,pk=partido_pk)
    partido.estado = 'finalizado'
    partido.save()
    url = reverse('vista_general:fechas_torneo',kwargs={'pk':partido.torneo.pk})
    return f'!Partido {partido.equipo_local.nombre} vs {partido.equipo_visitante.nombre} ha finalizado con exito!',url

def postRegistroIncidenciaPartidoBD(periodo,minutos,accion,jugador_id,partido_id,goles_local,goles_visitante):
    partido = get_object_or_404(Partido,pk=partido_id)

    # Opcional: Limpiar incidencias previas si es una edición
    partido.goles_local = 0
    partido.goles_visitante = 0
    IncidenciaPartido.objects.filter(partido=partido).delete()

    goles_total_marcadores = int(goles_local) + int(goles_visitante) 
    if  accion.count('gol') != goles_total_marcadores:
        return {"error":'Error en el registro: El total de goles detallados en las incidencias no coincide con el marcador final. Por favor, verifique y actualice los datos para guardar.'}
    
    jugadores_quesyset = Usuario.objects.filter(pk__in=jugador_id)
    jugadores_diccionario = { str(jugador.id): jugador for jugador in jugadores_quesyset }
    
    for jugador_ids,minuto,action,period in zip(jugador_id,minutos,accion,periodo):
        jugador = jugadores_diccionario.get(str(jugador_ids))
        if not jugador: print('Error no se encontró el id del jugador')

        minuto_real = int(minuto) + 20 if int(period) == 2 else int(minuto)

        IncidenciaPartido.objects.create(
            partido=partido,jugador=jugador,tipo=action,
            minuto=minuto_real,periodo=period
        )

        if action == 'gol':
            Goleador.objects.create(partido_id=partido_id,jugador=jugador,
                    equipo = jugador.equipos,minuto = minuto_real
            )
            if partido.equipo_local == jugador.equipos:
                partido.goles_local += 1
            elif partido.equipo_visitante == jugador.equipos:
                partido.goles_visitante += 1
    partido.save() #Guardamos a lo ultimo par aahorrar recursos         
    return {'exito':f'Registro del partido {partido.equipo_local} vs {partido.equipo_visitante} finalizado exitosamete'}

def registroMarcadorPartido(partido_id,goles_local,goles_visitante):
    partido = get_object_or_404(Partido,pk=partido_id)
    if goles_local and goles_visitante:
        partido.goles_local = goles_local
        partido.goles_visitante = goles_visitante
        partido.save()
        return {'exito':f'Registro del marcador para partido el {partido} finalizado correctamente'}
    return {'error':f'Ha ocurrido un error en el registro del marcador'}