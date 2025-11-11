from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from fase_de_grupos.models import EquipoGrupo
from Torneo.models import Torneo
from partidos.models import Partido

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
            resultados_queryset = Partido.objects.filter(estado="finalizado",torneo=torneo,grupo__nombre=self.kwargs["grupo"])
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
        try:
            partidos = Partido.objects.filter(torneo__pk=self.kwargs["torneo_pk"],grupo__nombre=self.kwargs["grupo"],estado="programado")
            data_partidos = []
            if partidos.exists():
                for partido in partidos:
                    data_partidos.append({
                        "localteam": partido.equipo_local.nombre,
                        'localteamlogo': partido.equipo_local.escudo.url if partido.equipo_local.escudo else "",
                        "awayteam": partido.equipo_visitante.nombre,
                        "awayteamlogo": partido.equipo_visitante.escudo.url if partido.equipo_visitante.escudo else "",
                        "cancha": partido.cancha,
                        "fecha_partido": partido.fecha_hora
                    })
                return JsonResponse({"fixtures":data_partidos})
            else:
                return JsonResponse({"error":"No hay partidos programado hasta ahora."})
        except Exception as e:
            return JsonResponse({"error":str(e)})