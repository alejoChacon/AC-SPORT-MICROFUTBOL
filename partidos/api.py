from django.views import View
from django.http import JsonResponse
from Torneo.models import Torneo
from .models import Partido
from . import services
import json
from datetime import datetime

class MisTorneosEnJuego(View):
    def get(self,request,*args,**kwargs):
        try:
            torneos_en_juego = Torneo.objects.filter(
                representante=self.request.user.get_full_name(),
                estado = "en_curso").values_list('id','nombre')
            return JsonResponse({
                'message':list(torneos_en_juego),
            })
        except Torneo.DoesNotExist:
            return JsonResponse({'error':'Torneos no encontrados'},status=404)
        except Exception as e:
             return JsonResponse({'error':str(e)},status=500)
        
class Jornadas(View):
    def get(self,request,*args,**kwargs):
        try:
            jornadas = Partido.objects.filter(torneo_id=kwargs['torneo_id']).order_by('jornada').values_list('jornada',flat=True).distinct()
            print(jornadas)
            return JsonResponse({'jornadas':list(jornadas)},safe=True)
        except Exception as e:
            print('Error: ',str(e))
            return JsonResponse({'error':str(e)},status=500)
        
class PartidosPorJornadas(View):
    def get(self,request,*args,**kwargs):
        try:
            partidos = services.obtener_partidos_por_jornadas(kwargs['torneo_id'],kwargs['jornada'])
            return JsonResponse({'partidos':partidos},safe=True)
        except Exception as e:
            return JsonResponse({'error':str(e)})
        
class AgendarPartido(View):
    def post(self,request,*args,**kwargs):
        try:
            print('Aqui está entrando')
            data = json.loads(request.body)
            partido_id = data.get('partido_id')
            fecha = data.get('fecha')
            hora = data.get('hora')
            cancha = data.get('cancha')
            print(partido_id,fecha,hora,cancha)
            partido = services.fixture_agendarpartidos(partido_id,fecha,hora,cancha)
            return JsonResponse({'message':partido})
        except Exception as e:
            print('\n ---------------------------------------------- \n Error: ',str(e))
            return JsonResponse({"error":'Ha ocurrido un problema con la informacion enviada, no se ha podido procesar la informacion'},status=500)