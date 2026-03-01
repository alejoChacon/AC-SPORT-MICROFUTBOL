from django.shortcuts import redirect
from django.contrib import messages
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from django.db import transaction
from . import services
import json

class PeticionIncidenciaPartido(LoginRequiredMixin,View):
    def post(self,request,*args,**kwargs):
        try:
            data = json.loads(request.body)
            partidoPK = data.get('partido_id')
            jugadorId = data.get('jugador_id')
            accion = data.get('accion')
            minuto = data.get('minuto')
            periodo = data.get('periodo')
            locacion = data.get('locacion')
            if all([partidoPK,jugadorId,accion,minuto,periodo,locacion]):
                datos = services.incidencia_de_partido_en_vivo(partidoPK=partidoPK,jugadorPk=jugadorId,accion=accion,minuto=minuto,periodo=periodo,locacion=locacion)
                return JsonResponse({'message':datos},safe=True)
        except Exception as e:
            return JsonResponse({'error':str(e)},status=500)
        
class EliminarSucesoDelPartidoEnVivo(LoginRequiredMixin,View):
    def post(self,request,*args,**kwargs):
        try:
            data = json.loads(request.body)
            incidencia_pk = data.get('incidencia_pk',)
            partido_pk = data.get('partido_pk',)
            eliminar_suceso,datos = services.eliminar_incidencia_del_partido(incidencia_pk,partido_pk)
            return JsonResponse({'exito':eliminar_suceso,'datos':datos},safe=True)
        except Exception as e:
            return JsonResponse({'error':str(e)},status=500)

class MarcadorEnVivo(LoginRequiredMixin,View):

    def get(self,request,*args,**kwargs):
        partido_id = self.kwargs['partido_pk']
        if partido_id:
            datos = services.marcador_en_Vivo(partido_id)
            return JsonResponse({'dato':datos})
        return JsonResponse({'error':'ha ocurrido un error, forbbiden the paremeter en the URL'})
    
class GuardarActa(LoginRequiredMixin,View):
    def post(self,request,*args,**kwargs):
        try:
            data = json.loads(request.body)
            partido_pk = data.get('partido_pk')
            if partido_pk:
                message,url = services.guardarActa(partido_pk)
                return JsonResponse({'exito':message,'url':url})
            else:
                return JsonResponse({'error':' Partido pk doesnt found'},status=404)
        except Exception as e:
            return JsonResponse({'error':str(e)},status=500)
        
class SucesosDElPartidoBeforeplaying(LoginRequiredMixin,View):
    def get(self,request,*args,**kwargs):
        try:
            partido = self.kwargs['partido_pk']
            datos = services.incidencias_del_partido(partidoPk=partido)
            return JsonResponse({'message':datos})
        except Exception as e:
            return JsonResponse({'error':str(e)})
        
class GestionActa(LoginRequiredMixin,View):
    def post(self,request,*args,**kwargs):
        try:
            goles_local = request.POST.get('goles_local')
            goles_visitante = request.POST.get('goles_visitante')
            periodo = request.POST.getlist('periodo[]')
            jugadores_id = request.POST.getlist('jugador[]')
            tipos = request.POST.getlist('tipo[]')
            minutos_lista = request.POST.getlist('minuto[]')
            torneo_pk = request.POST.get('torneo_pk')
            jornada = request.POST.get('jornada')
            partido_id = request.POST.get('partido_id')
            with transaction.atomic():
                if all([periodo,jugadores_id,tipos,minutos_lista,torneo_pk,jornada,partido_id]):
                    mensaje = services.postRegistroIncidenciaPartidoBD(periodo=periodo,jugador_id=jugadores_id,accion=tipos,minutos=minutos_lista,partido_id=partido_id,goles_local=goles_local,goles_visitante=goles_visitante)
                    if 'exito' in mensaje:
                        messages.success(request,mensaje['exito'])
                        services.guardarActa(partido_pk=partido_id)
                    else:
                        messages.error(request,mensaje['error'])
                    return redirect('vista_general:registrarmarcador',torneo_pk=torneo_pk,jornada=jornada)
                
                elif all([partido_id,goles_local,goles_visitante]):
                    mensaje = services.registroMarcadorPartido(partido_id=partido_id,goles_local=goles_local,goles_visitante=goles_visitante)
                    if 'error' in mensaje:
                        messages.error(request,mensaje['error'])
                    elif 'exito' in mensaje:
                        messages.success(request,mensaje['exito'])
                    return redirect('vista_general:registrarmarcador',torneo_pk=torneo_pk,jornada=jornada)
            print('Hubo un error en la recopilacion de datos')
        except Exception as e:
            print('Error: ',str(e))
