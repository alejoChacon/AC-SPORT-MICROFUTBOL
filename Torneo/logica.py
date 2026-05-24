from django.views import View
from django.urls import reverse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from fase_de_grupos.models import EquipoGrupo,Grupo
from Torneo.models import Torneo,Equipo
from partidos.models import Partido
from usuarios.models import Usuario
from django.db.models import Count,Q
from django.db import transaction
from .services import generar_grupos_torneo,generar_fixture
#import locale
#locale.setlocale(locale.LC_TIME, 'es_CO.UTF-8') 

class CargaPosiciones(LoginRequiredMixin,View):
    def get(self,request,*args,**kwars):
        try:
            equipos = EquipoGrupo.objects.filter(grupo__nombre=self.kwargs["grupo"],grupo__torneo__pk=self.kwargs["torneo_pk"]).select_related("equipo").order_by("-puntos", "-goles_favor")
            equipos_data = []
            for e in equipos:
                equipos_data.append({
                    "equipo": e.equipo.nombre,
                    "puntos": e.puntos,
                    "pj": e.partidos_jugados,
                    "pg": e.partidos_ganados,
                    "pp": e.partidos_perdidos,
                    "pe": e.partidos_empatados,
                    "gf": e.goles_favor,
                    "gc": e.goles_contra,
                    "dg": e.diferencias_goles
                })
            return JsonResponse({"equipos":equipos_data})
        except EquipoGrupo.DoesNotExist:
            return JsonResponse({"error":"No se pudo encontrar ese modelo"})
        except Exception as e:
            return JsonResponse({"error":str(e)})
        
class CargarResultados(LoginRequiredMixin,View):
    def get(self,request,*args,**kwargs):
        try:
            torneo = Torneo.objects.filter(pk=self.kwargs["torneo_pk"]).first()
            resultados_queryset = Partido.objects.filter(estado="finalizado",torneo=torneo,grupo__nombre=self.kwargs["grupo"],jornada=self.kwargs['fecha'])
            resultados = []
            for partido in resultados_queryset:
                resultados.append({
                    "equipolocal_escudo": partido.equipo_local.escudo.url if partido.equipo_local.escudo else "",
                    "equipolocal_nombre": partido.equipo_local.nombre,
                    "equipolocal_goles": partido.goles_local,
                    "equipoVisitante_escudo": partido.equipo_visitante.escudo.url if partido.equipo_visitante.escudo else "",
                    "equipoVisitante_nombre": partido.equipo_visitante.nombre,
                    "equipoVisitante_goles": partido.goles_visitante
                })
            return JsonResponse({"resultados":resultados})
        except Torneo.DoesNotExist:
            return JsonResponse({"error":"Torneo no fue encontrado"})
        except Exception as e:
            return JsonResponse({"error":str(e)})
          
class CargarPartidos(LoginRequiredMixin,View):
    def get(self,request,*args,**kwargs):
        print('---------------------------------------------------------------------------------------------')
        print('Tomando datos de los partidos')
        try:
            partidos = Partido.objects.filter(Q(estado="programado")|Q(estado='finalizado')|Q(estado='pendiente'),torneo__pk=self.kwargs["torneo_pk"],grupo__nombre=self.kwargs["grupo"],jornada=self.kwargs['fecha'])
            data_partidos = []
            if partidos.exists():
                for partido in partidos:
                    fecha_formateada = partido.fecha_hora.strftime("%d de %B del %Y %I:%M") if partido.fecha_hora else 'N/A'
                    data_partidos.append({
                        "localteam": partido.equipo_local.nombre,
                        'localteamlogo': partido.equipo_local.escudo.url if partido.equipo_local.escudo else "",
                        "awayteam": partido.equipo_visitante.nombre,
                        "awayteamlogo": partido.equipo_visitante.escudo.url if partido.equipo_visitante.escudo else "",
                        "cancha": partido.cancha if partido.cancha else 'N/A',
                        "fecha_partido": fecha_formateada
                    })
                return JsonResponse({"fixtures":data_partidos})
            else:
                print('Hubo un error pero toca encontrarlo')
                return JsonResponse({"error":"No hay partidos programado hasta ahora."})
        except Exception as e:
            return JsonResponse({"error":str(e)})
        
class Goleador(LoginRequiredMixin,View):
    def get(self,request,*args,**kwargs):
        try:
            anotadores_max = Usuario.objects.filter(goles__es_autogol=False,
                            goles__partido__torneo=self.kwargs["torneo_pk"]).annotate(
                            total_goles=Count('goles')).order_by('-total_goles')
            anotadores = []
            for jugador in anotadores_max:
                anotadores.append({
                    "nombre": jugador.get_full_name(),
                    "foto": jugador.foto.url if jugador.foto else "",
                    "equipo": jugador.equipos.nombre,
                    "escudo": jugador.equipos.escudo.url if jugador.equipos.escudo else "",
                    "goles": jugador.total_goles
                })
            return JsonResponse({"goleadores":anotadores})
        except Exception as e:
            return JsonResponse({"error":str(e)})
        
class EstadoTorneo(LoginRequiredMixin,View):
    def post(self,request,*args,**kwargs):
        try:
            with transaction.atomic():
                torneo_pk = request.POST.get('torneo_pk',False)
                cantidad_grupo = int(request.POST.get('cantidad-grupo'))
                cantidad_equipos_clasificacion = request.POST.get('cantidad_clasificacion')
                torneo = generar_grupos_torneo(torneo_pk,cantidad_grupo)
                generar_fixture(torneo.pk)
                url = reverse('torneo:torneoactivo',kwargs={'pk':torneo.pk})
                return JsonResponse({
                    'exito':'Grupos creados correctamente',
                    'url':url
                })
        except ValueError as e:
            return JsonResponse({'error': str(e)}, status=400)
        except Exception as e:
            print(str(e))
            return JsonResponse({'error':str(e)},status=500)