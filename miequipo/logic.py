from django.views.generic import View
from Torneo.models import Equipo
from usuarios.models import Usuario
from django.http import JsonResponse
from django.db.models import Q
from .models import Alineacion
from django.contrib.auth.mixins import LoginRequiredMixin
import json
import random

class SearchTeam(View):
    def get(self,request,*args,**kwargs):
        equipos_menos_de_10_jugadores = Equipo.objects.filter(Q(jugadores__lt=10)|Q(jugadores__isnull=True)).values_list('id','nombre','capitan__first_name').distinct()
        equipos_menos_de_10_jugadores = list(equipos_menos_de_10_jugadores)
        return JsonResponse(equipos_menos_de_10_jugadores,safe=False)
    
class AlineacionEquipo(LoginRequiredMixin,View):
    def post(self,request,*args,**kwargs):
        try:
            data = json.loads(request.body)
            equipo_pk = data.get('equipo_pk')
            arquero_pk = data.get('portero')
            cierre_pk = data.get('cierre')
            ala_izq_pk = data.get('ala-izq')
            ala_der_pk = data.get('ala-der')
            pivot_pk = data.get('pivot')
            print(f'Informacion, Portero {arquero_pk}| Cierre {cierre_pk}| Ala izquierda {ala_izq_pk}| Ala derecha {ala_der_pk}| Pivot: {pivot_pk}')
            alineacion, created = Alineacion.objects.get_or_create(
               equipo_id=equipo_pk,
               defaults={
                   'portero_id':arquero_pk,
                   'cierre_id':cierre_pk,
                   'ala_izq_id':ala_izq_pk,
                   'ala_der_id':ala_der_pk,
                   'pivot_id':pivot_pk
               }
            )
            if created:
                print('Se creo bien')
                return JsonResponse({'exito':f'Alineacion del equipo {alineacion.equipo.nombre} ha sido creada correctamente'})
            else:
                alineacion.portero_id = arquero_pk
                alineacion.cierre_id = cierre_pk
                alineacion.ala_izq_id = ala_izq_pk
                alineacion.ala_der_id = ala_der_pk
                alineacion.pivot_id = pivot_pk
                alineacion.save()
                return JsonResponse({'exito':f'Se ha actualizado la alineacion del equipo {alineacion.equipo.nombre}'})
        except Exception as e:
            print('Error: ',str(e))
            return JsonResponse({'error':str(e)})
        
class AbandonarEquipo(LoginRequiredMixin,View):
    def get(self,request,*args,**kwargs):
        try:
            user = Usuario.objects.get(pk=self.request.user.pk)
            if user.equipos.capitan == user:
                equipo = user.equipos
                id_jugadores = equipo.jugadores.exclude(pk=user.pk).values_list('id',flat=True)
                print(id_jugadores)
                id_escogido = random.choice(id_jugadores)
                print(id_escogido)
                equipo.capitan_id = id_escogido
                equipo.save()
            user.equipos = None
            user.save()
            return JsonResponse({'exito':f'{user.get_full_name()} ha abandonado el equipo'})
        except Exception as e:
            return JsonResponse({'error':str(e)})
        
class Agregarjugador(LoginRequiredMixin,View):
    def get(self,request,*args,**kwargs):
        try:
            freeplayers = Usuario.objects.filter(equipos__isnull=True,is_superuser=False).values_list('id','first_name','last_name','posicion','foto')
            return JsonResponse({'jugadores':list(freeplayers)})
        except Exception as e:
            return JsonResponse({"error":str(e)})